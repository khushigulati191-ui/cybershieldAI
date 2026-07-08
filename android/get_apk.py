
import re
from ssl import Options

from bs4 import BeautifulSoup

from package import get_package_name

def get_latest_version(package_name):
    import requests
    from google_play_scraper import app
    results = app(package_name, lang='en', country='us')
    version = results.get('version')
    if not version:
        version = "Unknown"
    
    return version

def name(app_name,app_version):
    from google_play_scraper import search,app
    try:
        results = search(
            app_name,
            lang="en",
            country="us",
            n_hits=1)
        APP = results[0]
        official_name = APP["title"]
        developer =  APP["developer"]
        return {
            "official_name": official_name,
            "developer": developer}

    
    except Exception as e:
        return {
            "error": str(e)
        }
    
def apk(package_name):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    import time
    from email.utils import quote


    # options = Options()
    # options.add_argument("--start-maximized")
    # options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option("useAutomationExtension", False)

    # driver = webdriver.Chrome(options=options)
    # import undetected_chromedriver as uc

    options = Options()
    
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option(
        "excludeSwitches", ["enable-automation"]
    )
    options.add_experimental_option(
        "useAutomationExtension", False
    )

    driver = webdriver.Chrome(options=options)

    url = (
            f"https://www.apkmirror.com/?post_type=app_release&searchtype=apk&s={quote(package_name)}"
        )
    driver.get(url)

    time.sleep(5)

    print(driver.title)
    # print(driver.page_source[:500])
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(driver.page_source, "html.parser")

    first = soup.select_one("a.fontBlack")

    if first is None:
        print("No APK found")
        driver.quit()
        return None

    apk_page = "https://www.apkmirror.com" + first["href"]
    driver.get(apk_page)

    import re

    match = re.search(r'(\d+(?:-\d+)+)-release', apk_page)

    if match:
        version = match.group(1).replace("-", ".")
    else:
        version = None

    return {
    "package_name": package_name,
    "version": version,
    "apk_page": apk_page,

}

    driver.quit()

# package_name = "com.whatsapp"

# result = get_latest_apkmirror(package_name)

# if result:
#     print("Latest Version:", result["version"])
#     print("APKMirror Page:", result["page_url"])
# else:
#     print("App not found")
    
result = get_package_name("Whatsapp Messenger")
print(f"Package name: {result}")

# apks = apk("Whatsapp Messenger")
# print(apks)

