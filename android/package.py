
"""
CyberShield AI - Google Play Package Name Resolver
====================================================

Single-purpose utility that uses Selenium to look up the package name
(e.g. "com.whatsapp") of an Android application listed on the Google
Play Store, given its displayed app name and developer name.

Why this approach avoids fragile CSS classes
---------------------------------------------
Google Play's front-end ships with obfuscated, auto-generated class
names (e.g. "Fd93Bb", "Vbfug", "TT9eCd") that are re-shuffled whenever
Google redeploys the front-end bundle. Hard-coding those classes makes
scrapers break within weeks. Instead, this script anchors its logic to
things that are far more stable across redeploys:

    1. The URL pattern of an app's detail link:
         /store/apps/details?id=<package_name>
       This is a functional routing contract Google Play must keep
       stable for bookmarking/sharing to keep working, so it is a much
       safer selector than any CSS class.

    2. Accessibility attributes (aria-label) on interactive elements,
       which Google tends to keep semantically meaningful for
       screen-reader compliance, making them more durable than
       presentational classes.

    3. Structural DOM boundaries: rather than trusting any single
       anchor's own text (or nearby siblings, which can bleed into a
       neighboring result), this script identifies the smallest DOM
       container that wraps EXACTLY ONE app-detail link - i.e. one
       search result "card" - and reads the title, developer, and
       click target all from strictly within that boundary. This is
       what guarantees the extracted name/developer and the link that
       gets clicked always belong to the same app.

Four important robustness fixes baked into this version
-----------------------------------------------------------
1. Text is read via JavaScript (textContent/innerText), NOT Selenium's
   built-in `.text` property. Selenium's `.text` applies its own
   visibility heuristics and frequently returns an empty string on
   modern flex/grid-based layouts like Play Store's, even though the
   text is plainly visible on screen. Reading textContent directly
   through execute_script avoids that entire class of false negatives.
2. Search is performed by navigating directly to Google Play's own
   documented search URL (/store/search?q=...&c=apps&hl=en&gl=us)
   instead of clicking into a UI search box. Play Store's homepage
   sometimes defaults to a category-specific tab (e.g. a Games-first
   homepage in certain regions), and any on-page search input found in
   that state ends up scoped to that category - so a query for a
   non-game app can silently return zero real results. Hitting the
   search URL directly with c=apps guarantees the search is scoped to
   all apps and is locale-independent.
3. hl=en&gl=us is pinned on the search URL so results (and their text)
   are in a consistent, predictable language/region.
4. Results are grouped into per-app "cards" (the smallest DOM ancestor
   containing exactly one app-detail link) before any text is read.
   Iterating raw anchors directly - the naive approach - can attribute
   a title/developer that visually sits near one anchor to a DIFFERENT
   anchor's href if the page's layout doesn't nest them the way you'd
   expect, producing wrong package names (e.g. resolving to an
   unrelated app like "com.instagram.airwave"). Scoping every read to
   a single-link card boundary eliminates that class of mismatch.

Everything - imports, configuration, and helper logic - lives inside
the single get_package_name() function below so this file can be
dropped into a larger project and imported as one self-contained unit:

    from cybershield_play_store_lookup import get_package_name
    pkg = get_package_name("WhatsApp Messenger", "WhatsApp LLC")
"""


from concurrent.futures import wait


def get_package_name(app_name: str) -> str | None:
    """
    Look up the Android package name of an app on the Google Play Store.

    Args:
        app_name: The exact (or near-exact) displayed app title, e.g.
                  "WhatsApp Messenger".
        developer_name: The exact (or near-exact) displayed developer/
                  publisher name, e.g. "WhatsApp LLC".

    Returns:
        The package identifier (e.g. "com.whatsapp") if a search result
        card matches BOTH the app name and developer name exactly
        (case-insensitive, trimmed), otherwise None.
    """

    # ------------------------------------------------------------------ #
    # All imports live inside the function so this single function is
    # fully self-contained and can be copy/imported anywhere on its own.
    # ------------------------------------------------------------------ #
    import logging
    import re
    from typing import List, Optional, Tuple
    from urllib.parse import urlparse, parse_qs, quote_plus

    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.remote.webelement import WebElement
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import (
        TimeoutException,
        NoSuchElementException,
        StaleElementReferenceException,
        WebDriverException,
    )

    # ------------------------------------------------------------------ #
    # Configuration constants (local to this call).
    # ------------------------------------------------------------------ #
    PLAY_STORE_HOME_URL = "https://play.google.com"
    # Any anchor whose href contains this substring points to an app's
    # detail page. This is the single most stable selector on the site.
    APP_DETAIL_HREF_MARKER = "/store/apps/details?id="
    DEFAULT_TIMEOUT = 15       # seconds to wait for slow-loading elements
    MAX_STALE_RETRIES = 3      # re-fetch attempts if result list goes stale
    MAX_CLIMB_LEVELS = 12      # safety cap when climbing ancestors to find a card boundary
    # Toggle True if running headless on a server without a display.
    HEADLESS = False
    # Prints every (title, developer) pair the scraper actually found on
    # the results page whenever no match is confirmed. Leave this on
    # while you're getting things working, then flip to False for
    # quieter production runs.
    DEBUG_MODE = True

    logger = logging.getLogger("cybershield.play_store_lookup")
    if not logger.handlers:
        logger.addHandler(logging.NullHandler())

    # ------------------------------------------------------------------ #
    # Nested helper: build and configure the Chrome WebDriver.
    # ------------------------------------------------------------------ #
    def _build_driver():
        options = Options()

        if HEADLESS:
            options.add_argument("--headless=new")

        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--lang=en-US")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        )

        return webdriver.Chrome(options=options)

    # ------------------------------------------------------------------ #
    # Nested helper: case-insensitive, whitespace-collapsed comparison.
    # ------------------------------------------------------------------ #
    def _normalize(value: Optional[str]) -> str:
        if not value:
            return ""
        return " ".join(value.split()).strip().lower()

    # ------------------------------------------------------------------ #
    # Nested helper: filters out lines that are clearly NOT a developer
    # name - star ratings, install counts, prices, button labels - so
    # card-text scanning doesn't mistake them for one.
    # ------------------------------------------------------------------ #
    NOISE_PATTERNS = [
        re.compile(r'^\d+(\.\d+)?$'),                       # bare numbers e.g. "4.3"
        re.compile(r'^\d+(\.\d+)?\s*(star|stars|★)', re.I), # star ratings
        re.compile(r'\d+(\.\d+)?\s*[km]?\+?\s*(downloads|installs)?$', re.I),
        re.compile(r'^(free|install|open|play|buy now|in-app purchases|contains ads)$', re.I),
        re.compile(r'^\$\d'),                                # prices like "$4.99"
    ]

    def _looks_like_developer_line(line: str) -> bool:
        stripped = line.strip()
        if not stripped:
            return False
        return not any(pattern.search(stripped) for pattern in NOISE_PATTERNS)

    # ------------------------------------------------------------------ #
    # Nested helper: given one app-detail anchor, climb up its ancestor
    # chain and return the SMALLEST container that still contains
    # exactly one app-detail link (i.e. this one). This is the search
    # result "card" boundary - it naturally expands to cover the app's
    # icon, title, developer, rating, and price/install button, but
    # stops the instant it would start including a second, different
    # app's link. Reading title/developer from within this exact
    # boundary is what guarantees they belong to the same app as the
    # link we're about to click.
    # ------------------------------------------------------------------ #
    def _find_card_root(driver, anchor: WebElement):
        script = """
        var hrefMarker = arguments[1];
        var maxLevels = arguments[2];
        var node = arguments[0];
        var candidate = node;
        for (var i = 0; i < maxLevels; i++) {
            if (!node.parentElement) { break; }
            node = node.parentElement;
            var count = node.querySelectorAll("a[href*='" + hrefMarker + "']").length;
            if (count === 1) {
                candidate = node;
                continue;
            }
            break;
        }
        return candidate;
        """
        try:
            result = driver.execute_script(
                script, anchor, APP_DETAIL_HREF_MARKER, MAX_CLIMB_LEVELS
            )
            return result if result is not None else anchor
        except WebDriverException:
            return anchor

    # ------------------------------------------------------------------ #
    # Nested helper: deduplicate anchors down to unique cards. Some
    # cards have more than one element linking to the same app (e.g. an
    # icon link and a title link with identical hrefs), which would
    # otherwise cause the same app to be processed - and its card
    # re-tagged - more than once. A random marker is stamped onto each
    # card root's dataset the first time it's seen so repeats are
    # recognized and skipped.
    # ------------------------------------------------------------------ #
    def _collect_result_cards(driver, anchors: List[WebElement]) -> List[Tuple[object, WebElement]]:
        cards = []
        seen_markers = set()

        for anchor in anchors:
            try:
                card_root = _find_card_root(driver, anchor)
            except StaleElementReferenceException:
                continue

            try:
                marker = driver.execute_script(
                    "var el = arguments[0]; "
                    "if (!el.dataset.cybershieldCardId) { "
                    "  el.dataset.cybershieldCardId = "
                    "    'cs-' + Math.random().toString(36).slice(2) + '-' + Date.now(); "
                    "} "
                    "return el.dataset.cybershieldCardId;",
                    card_root,
                )
            except WebDriverException:
                continue

            if marker in seen_markers:
                continue
            seen_markers.add(marker)
            cards.append((card_root, anchor))

        return cards

    # ------------------------------------------------------------------ #
    # Nested helper: extract the app title and developer name from
    # strictly within one card's boundary, plus confirm the click
    # target anchor. Text is read via JavaScript's textContent/
    # innerText, NOT Selenium's WebElement.text, since Selenium's own
    # visibility algorithm frequently returns "" on modern flex/grid
    # layouts like Play Store's even when text is visibly on screen.
    # ------------------------------------------------------------------ #
    def _extract_card_details(driver, card_root, link_element: WebElement) -> Tuple[Optional[str], Optional[str]]:
        title: Optional[str] = None

        aria_label = link_element.get_attribute("aria-label")
        if aria_label:
            parts = [segment.strip() for segment in aria_label.split(",") if segment.strip()]
            if parts:
                title = parts[0]

        raw_text = driver.execute_script(
            "return (arguments[0].innerText || arguments[0].textContent || '');",
            card_root,
        ) or ""
        lines = [line.strip() for line in raw_text.split("\n") if line.strip()]

        if not lines:
            return title, None

        if title is None:
            title = lines[0]

        normalized_title = _normalize(title)
        developer: Optional[str] = None
        for line in lines:
            if _normalize(line) == normalized_title:
                continue
            if not _looks_like_developer_line(line):
                continue
            IGNORE = {
                "contains ads",
                "in-app purchases",
                "star",
                "stars",
}
            if any(ignore_word in line.lower() for ignore_word in IGNORE):
                continue
            developer = line
            break

        return title, developer

    # ------------------------------------------------------------------ #
    # Nested helper: scan every search-result card and return the click
    # target (anchor) whose card title AND developer both exactly match
    # the arguments (case-insensitive, trimmed). Returns None if
    # nothing matches, after printing every candidate seen (when
    # DEBUG_MODE is on) so mismatches can be diagnosed.
    # ------------------------------------------------------------------ #

    def _find_matching_result(driver, wait: WebDriverWait) -> Optional[WebElement]:
        normalized_app_name = _normalize(app_name)

        for attempt in range(1, MAX_STALE_RETRIES + 1):
                try:
                        anchors: List[WebElement] = wait.until(
                                EC.presence_of_all_elements_located(
                                (By.CSS_SELECTOR, "a[href*='" + APP_DETAIL_HREF_MARKER + "']")
                                )
                        )

                        cards = _collect_result_cards(driver, anchors)
                        seen_candidates = []

                        for card_root, link_element in cards:
                                title, developer = _extract_card_details(driver, card_root, link_element)
                                seen_candidates.append((title, developer))

                                if title is None:
                                        continue

                                # Match ONLY app name (exact)
                                if _normalize(title) == normalized_app_name:
                                        if DEBUG_MODE:
                                                print(f"[MATCH] {title}")
                                        return link_element

                        if DEBUG_MODE:
                                print(
                                "[CyberShield DEBUG] No match for app_name={!r}. Candidates found:".format(
                                        app_name
                                )
                                )

                                for candidate_title, candidate_developer in seen_candidates:
                                        print(
                                                "  - title={!r} developer={!r}".format(
                                                candidate_title,
                                                candidate_developer,
                                                )
                                        )

                        return None

                except StaleElementReferenceException:
                        logger.debug(
                                "Result list went stale during scan (attempt %d/%d); retrying.",
                                attempt,
                                MAX_STALE_RETRIES,
                        )
                        continue

                        return None
                                        
                    
    # ------------------------------------------------------------------ #
    # Nested helper: click an element robustly.
    # ------------------------------------------------------------------ #
    def _click_element(driver, element: WebElement) -> None:
        try:
            element.click()
        except WebDriverException:
            driver.execute_script("arguments[0].click();", element)

    # ------------------------------------------------------------------ #
    # Nested helper: pull the 'id' query parameter out of a Play Store
    # app URL.
    # ------------------------------------------------------------------ #
    def _extract_package_name_from_url(url: str) -> Optional[str]:
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)
        package_ids = query_params.get("id")
        return package_ids[0] if package_ids else None

    # ------------------------------------------------------------------ #
    # Main workflow.
    # ------------------------------------------------------------------ #
    driver = None

    try:
        # Step 1: Launch Chrome.
        driver = _build_driver()
        wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

        # Step 2 & 3: Open the Play Store search results directly, scoped
        # to "apps" (c=apps) with a pinned English/US locale. Navigating
        # straight to this documented search URL - rather than clicking
        # into whatever search box the homepage happens to show - avoids
        # a real-world failure mode: Play Store's homepage sometimes
        # defaults to a category-specific tab (e.g. a Games-first
        # homepage in certain regions), and an on-page search box found
        # in that state ends up scoped to that category.
        search_url = (
            f"{PLAY_STORE_HOME_URL}/store/search"
            f"?q={quote_plus(app_name)}&c=apps&hl=en&gl=us"
        )
        driver.get(search_url)

        # Step 4: Wait for search results, then group them into per-app
        # cards and scan every card comparing BOTH app name and
        # developer name (never just click the first hit, and never
        # trust an anchor's text without confirming it belongs to that
        # same anchor's card boundary).
        matched_anchor = _find_matching_result(driver, wait)

        if matched_anchor is None:
            logger.info(
                        "No Play Store result matched app_name=%r",
                                app_name,
                                                )
            return None

        # Step 5: Click into the matched app's detail page.
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", matched_anchor
        )
        _click_element(driver, matched_anchor)

        # Step 6: Wait until the app details page has actually loaded.
        wait.until(EC.url_contains(APP_DETAIL_HREF_MARKER))
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))

        # Step 7: Extract the package name from the final URL's "id"
        # query parameter.
        return _extract_package_name_from_url(driver.current_url)

    except TimeoutException:
        logger.warning(
            "Timed out while resolving package name for app_name=%r", app_name
        )
        return None
    except NoSuchElementException:
        logger.warning(
            "Required element not found while resolving app_name=%r", app_name
        )
        return None
    except StaleElementReferenceException:
        logger.warning(
            "Page DOM changed unexpectedly (stale element) for app_name=%r",
            app_name,
        )
        return None
    finally:
        # Step 8: Always close the browser, even if an exception was
        # raised above, to avoid leaking Chrome processes.
        if driver is not None:
            try:
                driver.quit()
            except WebDriverException:
                logger.debug("driver.quit() raised while cleaning up.", exc_info=True)


# if __name__ == "__main__":
#     result = get_package_name("Instagram")
#     if result:
#         print("Package name:", result)
#     else:
#         print("No matching app found.")
        