def find_metadata(package_name,):
    from google_play_scraper import search,app
    try:
        
        
        data = app(package_name, lang="en", country="us")

        details = app(
        package_name,
        lang="en",
        country="us"
    )
        

        return {
            "official_name": details["title"],
            "package_name": details["appId"],
            "developer": details["developer"],
            "version": details["version"],
            "version_code": details.get("versionCode"),
            "category": details["genre"],
            "installs": details["installs"],
            "rating": details["score"],
            "updated": details.get("updatedOn"),
            "description": details["summary"],
            "privacy_policy": details.get("privacyPolicy"),
            "data" : data
        }

    except Exception as e:
        return {
            "error": str(e)
        }   


