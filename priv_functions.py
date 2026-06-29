
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