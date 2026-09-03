def find_metadata(package_name):
    from google_play_scraper import app

    try:
        details = app(
            package_name,
            lang="en",
            country="us"
        )

        return {
            "official_name": details.get("title"),
            "package_name": details.get("appId"),
            "developer": details.get("developer"),
            "version": details.get("version"),
            "version_code": details.get("versionCode"),
            "category": details.get("genre"),
            "installs": details.get("installs"),
            "rating": details.get("score"),
            "updated": details.get("updatedOn"),
            "description": details.get("summary"),
            "privacy_policy": details.get("privacyPolicy"),
            "data": details
        }

    except Exception as e:
        return {
            "error": str(e),
            "data": None
        }