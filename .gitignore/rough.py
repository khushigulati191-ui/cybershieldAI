import requests

def get_ios_app(app_name):
    url = f"https://itunes.apple.com/search?term={app_name}&entity=software&limit=1"

    response = requests.get(url).json()

    if response["resultCount"] == 0:
        return None

    return response["results"][0]

print(get_ios_app("Instagram"))