def analyze_privacy_labels(metadata):
    """
    Apple privacy labels scoring.
    Returns score and detected labels.
    """

    labels = {
        "trackContent": metadata.get("trackContent", False),
        "trackData": metadata.get("trackData", False),
        "trackC2a": metadata.get("trackC2a", False)
    }

    if not any(labels.values()):
        score = 40
        status = "Data Not Collected"
    elif labels["trackData"]:
        score = 10
        status = "Data Used to Track You"
    elif labels["trackContent"] or labels["trackC2a"]:
        score = 20
        status = "Data Linked to You"
    else:
        score = 30
        status = "Data Not Linked to You"

    return {
        "score": score,
        "label score" : f"{score}/40",
        "status": status,
        "labels": labels
    }

def analyze_privacy_policy(metadata):
    policy = metadata.get("privacyPolicyUrl")

    if policy:
        score = 20
        if policy.startswith("https://"):
            score = 30
            status = "HTTPS Privacy Policy"
        else:
            score = 25
            status = "HTTP Privacy Policy"

    else:
        score = 0
        status = "Privacy Policy Missing"

    return {
        "score": score,
        "policy score" : f"{score}/30",
        "status": status,
        "url": policy
    }


def analyze_data_collection(metadata):
    indicators = []

    if metadata.get("trackContent"):
        indicators.append("Collects Usage Data")

    if metadata.get("trackC2a"):
        indicators.append("Collects Contact Information")

    if metadata.get("trackData"):
        indicators.append("Collects Tracking Data")

    count = len(indicators)

    if count == 0:
        score = 20
    elif count == 1:
        score = 15
    elif count == 2:
        score = 10
    else:
        score = 5

    return {
        "score": score,
        "indicator score" : f"{score}/20",
        "indicators": indicators,
    }

def analyze_tracking_indicators(metadata):
    tracking = metadata.get("trackData", False)

    if tracking:
        score = 0
        status = "Tracking Detected"
    else:
        score = 10
        status = "No Tracking Detected"

    return {
        "score": score,
        "tracking indicator" : f"{score}/10",
        "status": status,
        
    }