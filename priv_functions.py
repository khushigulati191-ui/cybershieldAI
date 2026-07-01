
def cookies_check(final_url):
    score = 0
    session_cookies = []
    persistent_cookies = []
    third_party_cookies = []
    first_party_cookies = []
    cookies_name = []
    from playwright.sync_api import sync_playwright
    from urllib.parse import urlparse
    main_domain = urlparse(final_url).hostname
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(final_url,wait_until="domcontentloaded",timeout=60000)
        cookies = page.context.cookies()     #cookies is a nested dictionary 
        no_of_cookies = len(cookies)
        if no_of_cookies >15:
            score+=5
        elif no_of_cookies>5:
            score+=10
        else:
            score+=15
        for cookie in cookies:
            cookies_name.append(cookie['name'])
            if cookie['expires']!= None:
                persistent_cookies.append(cookie['name'])
            else:
                session_cookies.append(cookie['name'])
            if not cookie["domain"].endswith(main_domain):
                third_party_cookies.append(cookie["name"])
            else:
                first_party_cookies.append(cookie["name"])
        browser.close()
    return {
        "score" : score, "Cookies_score" : f"{score}/15" ,
        "Cookie_Count": no_of_cookies,
        "Session_Cookies": session_cookies ,
        "Persistent_Cookies": persistent_cookies,
        "Third_Party_Cookies": third_party_cookies,
        "First_Party_Cookies": first_party_cookies
    }

def third_party_trackers_check(final_url):
    import requests
    from bs4 import BeautifulSoup

    TRACKERS = {
        "Google Analytics": [
            "google-analytics.com",
            "googletagmanager.com",
            "gtag/js",
            "analytics.js"
        ],
        "Facebook Pixel": [
            "connect.facebook.net",
            "fbevents.js"
        ],
        "Hotjar": [
            "hotjar.com",
            "static.hotjar.com"
        ],
        "Mixpanel": [
            "mixpanel.com"
        ],
        "TikTok Pixel": [
            "analytics.tiktok.com",
            "tiktok.com"
        ],
        "DoubleClick": [
            "doubleclick.net"
        ]
    }

    html = requests.get(final_url, headers={"User-Agent":"Mozilla/5.0"}).text
    soup = BeautifulSoup(html, "html.parser")

    detected = set()

    for script in soup.find_all("script"):
        src = script.get("src")

        if not src:
            continue

        src = src.lower()

        for tracker, signatures in TRACKERS.items():
            if any(signature in src for signature in signatures):
                detected.add(tracker)

    count = len(detected)

    if count == 0:
        score = 25
    elif count <= 3:
        score = 15
    else:
        score = 5

    return {
        "score": score,
        "TPT_score": f"{score}/25",
        "Tracker Count": count,
        "Trackers": list(detected)
    }
    
def ads_check(final_url):
    score = 0
    import requests
    from bs4 import BeautifulSoup
    AD_NETWORKS = {
    "Google Ads": [
        "googleads.g.doubleclick.net",
        "adservice.google.com"
    ],

    "DoubleClick": [
        "doubleclick.net"
    ],

    "AdSense": [
        "pagead2.googlesyndication.com",
        "googlesyndication.com"
    ]}

    detected = set()

    try:
        response = requests.get(final_url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        tags = soup.find_all(["script", "iframe", "img", "link"])

        for tag in tags:
            url = (
                tag.get("src")
                or tag.get("href")
                or ""
            ).lower()

            for company, domains in AD_NETWORKS.items():

                for domain in domains:

                    if domain in url:
                        detected.add(company)

    except Exception:
        return {
            "score": 0,
            "detected": [],
            "status": "Unable to analyze"
        }

    if len(detected) == 0:
        score = 15
    elif len(detected)==1:
        score = 12
    elif len(detected) == 2:
        score = 9
    elif len(detected) ==3:
        score = 6
    else:
        score = 3

    return {
        "score": score,
        "ADS_score" : f"{score}/15",
        "detected": list(detected),
        "status": "Advertising networks found" if detected else "No advertising networks detected"
    }
    
def privacy_policy_check(final_url):
    import requests
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin
    score = 0
    keywords = [
        "privacy policy",
        "privacy",
        "privacy notice",
        "privacy statement",
        "data privacy"
    ]

    try:
        response = requests.get(final_url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a")

        found = False
        accessible = False
        policy_url = None

        for link in links:
            text = link.get_text(" ", strip=True).lower()
            href = (link.get("href") or "").lower()

            for keyword in keywords:
                if keyword in text or keyword in href:
                    found = True
                    accessible = True
                    policy_url = urljoin(final_url, link.get("href"))
                    break

            if found:
                break

        if found:
            score += 7

        if accessible:
            score += 3

        return {
            "score": score,
            "PPC_score": f"{score}/10",
            "privacy_policy_found": found,
            "accessible": accessible,
            "policy_url": policy_url
        }

    except Exception as e:
        return {
            "score": 0,
            "PPC_score": f"{score}/10",
            "error": str(e)
        }
    
def data_collection_indicators_check(final_url):
    score = 0
    import requests
    from bs4 import BeautifulSoup
    TRACKERS = {
    "googletagmanager.com",
    "google-analytics.com",
    "doubleclick.net",
    "facebook.net",
    "clarity.ms",
    "hotjar.com",
    "segment.com",
    "mixpanel.com",
    "amplitude.com",
}
    FINGERPRINT_KEYWORDS = [
    "fingerprintjs",
    "fingerprint2",
    "clientjs",
    "creepjs",
    "canvasfingerprint",
]
    SESSION_REPLAY = [
    "hotjar",
    "clarity",
    "fullstory",
    "smartlook",
    "mouseflow",
    "logrocket",
    "luckyorange",
]
    
    try:
        response = requests.get(final_url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        scripts = soup.find_all("script")

        trackers = []
        fingerprint = []
        session_replay= []

        trackers_found = False
        fingerprint_found = False
        session_replay_found = False

        for script in scripts:
            src = (script.get("src") or "").lower()
            for tracker in TRACKERS:
                if tracker in src:
                    trackers.append(tracker)
                    trackers_found = True

            for fingerprint in FINGERPRINT_KEYWORDS:
                if fingerprint in src:
                    fingerprint_found = True
                    fingerprint.append(fingerprint)

            for replay in SESSION_REPLAY:
                if replay in src:
                    session_replay_found = True
                    session_replay.append(replay)

        if len(trackers) == 0:
            score += 15
        elif len(trackers) < 3:
            score += 12
        elif len(trackers) <= 5:
            score += 9
        else:
            score += 6
        if fingerprint_found:
            score -= 3
        if session_replay_found:
            score -= 3

        return {
            "score": score,
            "data_collection_indicators_score": f"{score}/15",
            "tracker_count": len(trackers), 
            "trackers_found": trackers_found,
            "fingerprint_found": fingerprint_found,
            "session_replay_found": session_replay_found,
            "trackers": set(trackers),
            "fingerprint": set(fingerprint),
            "session_replay": set(session_replay)
        }
        
    except Exception as e:
        return {
            "score": 0,
            "data_collection_indicators_score": f"{score}/10",
            "error": str(e)
        }