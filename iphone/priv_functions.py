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
    policy = metadata.get("Privacy policy")

    if policy:
        if policy.startswith("https://"):
            score = 15
            status = "HTTPS Privacy Policy Available"

        else:
            score = 10
            status = "Privacy Policy Available but Not HTTPS"

    else:
        # Baseline score because actual URL detection
        # is not implemented yet.
        score = 5
        status = "Privacy Policy Expected, URL Not Verified"

    return {
        "score": score,
        "policy score": f"{score}/15",
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
        "status": status
    }

def analyze_advertisement(metadata):

    tracking_detected = metadata.get("trackData", False)

    # Collect available tracking-related information
    tracking_details = []

    if tracking_detected:
        tracking_details.append(
            "App Store privacy label indicates data may be used for tracking."
        )

    if tracking_detected:
        score = 5
        risk_level = "High"
        status = "Tracking-related advertising indicators detected"
    else:
        score = 15
        risk_level = "Low"
        status = "No tracking-related advertising indicators detected"

    return {
        "score": score,
        "advertisement_score": f"{score}/15",
        "status": status,
        "risk_level": risk_level,
        "tracking_detected": tracking_detected,
        "tracking_details": tracking_details
    }