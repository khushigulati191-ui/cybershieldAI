

def get_ios_app(app_name):
    import requests
    url = f"https://itunes.apple.com/search?term={app_name}&entity=software&limit=1"

    response = requests.get(url).json()

    if response["resultCount"] == 0:
        return None
    return response["results"][0]



def analyze_privacy_labels(app_data):
    """
    labels -> list of Apple privacy labels
    """
    labels = analyze_privacy_labels(
        app_data.get("privacy_labels", [])
    )
    
    if not labels:
        return {
            "status": "Data Not Collected",
            "score": 40
        }

    label_text = " ".join(labels).lower()

    if "track" in label_text:
        score = 10
        status = "Data Used to Track You"

    elif "linked" in label_text:
        score = 20
        status = "Data Linked to You"

    elif "not linked" in label_text:
        score = 30
        status = "Data Not Linked to You"

    else:
        score = 40
        status = "Data Not Collected"

    return {
        "status": status,
        "score": score,
        "labels": labels
    }