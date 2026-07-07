def metadata(app_name,app_version):
    from google_play_scraper import search,app
    try:
        results = search(
            app_name,
            lang="en",
            country="us",
            n_hits=1)
        print(results)

        APP = results[0]
        official_name = APP["title"]
        print(official_name)
        package_name =  APP["appId"]
        developer =  APP["developer"]

        details = app(
        package_name,
        lang="en",
        country="us"
    )
        if app_version != None:
            version = app_version
            version_code = None
        else:
            version = details["version"]
            version_code = details["versionCode"]

        return {
            "official_name": details["title"],
            "package_name": details["appId"],
            "developer": details["developer"],
            "version": version,
            "version_code": version_code,
            "category": details["genre"],
            "installs": details["installs"],
            "rating": details["score"],
            "updated": details["updatedOn"],
            "description": details["summary"],
            "privacy_policy": details.get("privacyPolicy")
        }

    except Exception as e:
        return {
            "error": str(e)
        }   
print(metadata("Instagram", None))

def apk_verification(app_name):
    """
    Verify the APK signature of the given app.

    Args:
        app_name (str): The name of the app to verify.

    Returns:
        bool: True if the APK signature is valid, False otherwise. also checks other security aspects of the app.
    """
    score = 0



    return {

    }

