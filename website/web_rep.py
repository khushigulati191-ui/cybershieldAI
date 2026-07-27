
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


# ============================================================
# 1. KNOWN SUSPICIOUS DOMAINS
# ============================================================

# Add domains that are known to be suspicious or malicious.
# The values represent how many points should be deducted.
def reputation(final_url):
    SUSPICIOUS_DOMAINS = {
        "example-phishing.com": {
            "deduction": 10,
            "reason": "Known phishing domain"
        },

        "fake-google-login.com": {
            "deduction": 10,
            "reason": "Known impersonation/phishing domain"
        },

        "suspicious-site.com": {
            "deduction": 5,
            "reason": "Reported as suspicious"
        }
    }


    # ============================================================
    # 2. SUSPICIOUS KEYWORDS
    # ============================================================

    # These keywords can be used as basic indicators.
    # This is NOT a replacement for a real threat intelligence API.

    SUSPICIOUS_KEYWORDS = [
        "phishing",
        "malware",
        "scam",
        "fraud",
        "fake",
        "credential theft"
    ]


    # ============================================================
    # 3. MAIN REPUTATION CHECK
    # ============================================================

    parsed_url = urlparse(final_url)
    domain = parsed_url.netloc.lower()

    # Remove www.
    domain = domain.replace("www.", "")

    # Start with maximum score
    reputation_score = 20

    findings = []

    # ========================================================
    # PARAMETER 1: THREAT REPUTATION (10 POINTS)
    # ========================================================

    threat_deduction = 0

    if domain in SUSPICIOUS_DOMAINS:

        threat_info = SUSPICIOUS_DOMAINS[domain]

        threat_deduction = threat_info["deduction"]

        reputation_score -= threat_deduction

        findings.append(
            f"Threat Reputation: {threat_info['reason']} "
            f"(-{threat_deduction} points)"
        )

    else:

        findings.append(
            "Threat Reputation: No known threats found "
            "in the local reputation database."
        )


    # ========================================================
    # PARAMETER 2: SEARCH PRESENCE (3 POINTS)
    # ========================================================

    # NOTE:
    # This is a simplified no-API implementation.
    # We check whether the website has a valid title and
    # meaningful content as a basic proxy for online presence.
    #
    # This does NOT actually check Google rankings.

    search_presence_deduction = 0

    try:

        response = requests.get(
            final_url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        if response.status_code == 200:

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            title = soup.title

            if title and title.get_text(strip=True):

                findings.append(
                    "Search Presence: Website has a valid "
                    "page title and accessible content."
                )

            else:

                search_presence_deduction = 1

                reputation_score -= search_presence_deduction

                findings.append(
                    "Search Presence: Website has no meaningful "
                    "page title (-1 point)."
                )

        else:

            search_presence_deduction = 2

            reputation_score -= search_presence_deduction

            findings.append(
                f"Search Presence: Website returned HTTP "
                f"status {response.status_code} (-2 points)."
            )

    except requests.RequestException:

        search_presence_deduction = 2

        reputation_score -= search_presence_deduction

        findings.append(
            "Search Presence: Website could not be reached "
            "(-2 points)."
        )


    # ========================================================
    # PARAMETER 3: IMPERSONATION RISK (4 POINTS)
    # ========================================================

    impersonation_deduction = 0

    # Basic keyword-based detection.
    # This checks whether the domain contains suspicious
    # impersonation-related words.

    impersonation_keywords = [
        "login",
        "verify",
        "secure",
        "account",
        "update",
        "support",
        "official"
    ]

    suspicious_words_found = []

    for word in impersonation_keywords:

        if word in domain:

            suspicious_words_found.append(word)


    if suspicious_words_found:

        impersonation_deduction = 2

        reputation_score -= impersonation_deduction

        findings.append(
            "Impersonation Risk: Domain contains potentially "
            "suspicious keywords: "
            + ", ".join(suspicious_words_found)
            + " (-2 points)."
        )

    else:

        findings.append(
            "Impersonation Risk: No obvious impersonation "
            "keywords detected in the domain."
        )


    # ========================================================
    # PARAMETER 4: ONLINE PRESENCE (3 POINTS)
    # ========================================================

    online_presence_deduction = 0

    try:

        response = requests.get(
            final_url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        page_text = soup.get_text(
            " ",
            strip=True
        ).lower()


        # ----------------------------------------------------
        # Check for basic business/contact information
        # ----------------------------------------------------

        contact_keywords = [
            "contact",
            "about us",
            "email",
            "phone",
            "address"
        ]

        contact_found = any(
            keyword in page_text
            for keyword in contact_keywords
        )


        # ----------------------------------------------------
        # Check for social media links
        # ----------------------------------------------------

        social_platforms = [
            "facebook.com",
            "instagram.com",
            "linkedin.com",
            "twitter.com",
            "x.com",
            "youtube.com"
        ]

        social_media_found = False

        for link in soup.find_all("a", href=True):

            href = link["href"].lower()

            if any(
                platform in href
                for platform in social_platforms
            ):

                social_media_found = True

                break


        # ----------------------------------------------------
        # Score Online Presence
        # ----------------------------------------------------

        if not contact_found and not social_media_found:

            online_presence_deduction = 2

            reputation_score -= online_presence_deduction

            findings.append(
                "Online Presence: No obvious contact/business "
                "information or social media links found "
                "(-2 points)."
            )

        elif not contact_found:

            online_presence_deduction = 1

            reputation_score -= online_presence_deduction

            findings.append(
                "Online Presence: Social media links found, "
                "but no obvious contact/business information "
                "was detected (-1 point)."
            )

        else:

            findings.append(
                "Online Presence: Website contains basic "
                "contact/business information."
            )


    except requests.RequestException:

        online_presence_deduction = 2

        reputation_score -= online_presence_deduction

        findings.append(
            "Online Presence: Unable to analyze website "
            "content (-2 points)."
        )


    # ========================================================
    # FINAL SCORE SAFETY
    # ========================================================

    # Never allow score below 0
    reputation_score = max(
        0,
        reputation_score
    )


    # ========================================================
    # DETERMINE FINAL STATUS
    # ========================================================

    if reputation_score >= 17:

        status = "Excellent"

    elif reputation_score >= 13:

        status = "Good"

    elif reputation_score >= 8:

        status = "Moderate Risk"

    elif reputation_score >= 4:

        status = "High Risk"

    else:

        status = "Critical Risk"


    # ========================================================
    # RETURN RESULTS
    # ========================================================

    return {
    # ========================================================
    # BASIC WEBSITE INFORMATION
    # ========================================================

    "url": final_url,
    "domain": domain,

    # ========================================================
    # FINAL REPUTATION RESULT
    # ========================================================

    "score" : reputation_score,
    "reputation_score": f"{reputation_score}/20",
    "status": status,

    # ========================================================
    # 1. THREAT REPUTATION
    # ========================================================

    "threat_reputation": {
        "maximum_points": 10,
        "points_deducted": threat_deduction,
        "domain_found_in_suspicious_database": (
            domain in SUSPICIOUS_DOMAINS
        ),
        "reason": (
            SUSPICIOUS_DOMAINS[domain]["reason"]
            if domain in SUSPICIOUS_DOMAINS
            else "No known threats found in the local reputation database."
        )
    },

    # ========================================================
    # 2. SEARCH / WEB PRESENCE
    # ========================================================

    "search_presence": {
        "maximum_points": 3,
        "points_deducted": search_presence_deduction,
        "website_accessible": (
            search_presence_deduction < 2
        ),
    },

    # ========================================================
    # 3. IMPERSONATION RISK
    # ========================================================

    "impersonation_risk": {
        "maximum_points": 4,
        "points_deducted": impersonation_deduction,
        "suspicious_keywords_found": suspicious_words_found,
        "risk_detected": (
            len(suspicious_words_found) > 0
        )
    },

    # ========================================================
    # 4. ONLINE PRESENCE
    # ========================================================

    "online_presence": {
        "maximum_points": 3,
        "points_deducted": online_presence_deduction,
        "contact_information_found": contact_found,
        "social_media_found": social_media_found,
    },

    # ========================================================
    # ALL HUMAN-READABLE FINDINGS
    # ========================================================

    "findings": findings
}