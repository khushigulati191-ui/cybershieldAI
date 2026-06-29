
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
        page.goto(final_url)
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
    

    