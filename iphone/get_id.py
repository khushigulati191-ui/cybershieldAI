import requests


def get_ios_app_ids(app_name):
    url = "https://itunes.apple.com/search"

    params = {
        "term": app_name,
        "entity": "software",
        "limit": 1
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        if data["resultCount"] == 0:
            return None

        app = data["results"][0]
        apple_id = app.get("trackId")
        lookup_url = f"https://itunes.apple.com/lookup?id={apple_id}"
        metadata = requests.get(lookup_url).json()["results"][0]
        return {
            "app_name": app.get("trackName"),
            "app_store_id": app.get("trackId"),
            "bundle_id": app.get("bundleId"),
            "developer": app.get("sellerName"),
            "metadata" : metadata
        }

    except Exception as e:
        print(f"Error: {e}")
        return None



result = get_ios_app_ids("hill climb racing")
if result:
    for k,v in result.items():
        print(f"{k} : {v}")
else:
    print("no")