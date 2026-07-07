from package import get_package_name


def apk(app_name,app_version):
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
    
result = get_package_name("WhatsApp Messenger")

print(f"Package name: {result}")