

# =========================
# SECURITY ANALYSIS
# =========================
def metadata_security(package_name):
    """
    Returns:
    {
        "score": int,
        "risk_level": str,
        "details": {...},
        "issues": [...],
        "recommendations": [...]
    }
    """
    from google_play_scraper import app
    from datetime import datetime
    import requests
    import re

    score = 0
    issues = []
    recommendations = []

    try:
        data = app(package_name, lang="en", country="in")
    except Exception as e:
        return {
            "score": 0,
            "risk_level": "Unknown",
            "details": {},
            "issues": [f"Unable to fetch metadata: {e}"],
            "recommendations": ["Verify package name."]
        }

    details = {}

    # =====================================================
    # 1. Developer Reputation (20)
    # =====================================================
    trusted_developers = [
        "Google LLC",
        "Meta Platforms, Inc.",
        "Microsoft Corporation",
        "Samsung Electronics Co., Ltd.",
        "Amazon Mobile LLC",
        "Adobe",
        "Netflix, Inc.",
        "WhatsApp LLC",
        "Telegram FZ-LLC",
        "Signal Foundation"
    ]

    developer = data.get("developer", "Unknown")
    details["developer"] = developer

    if developer in trusted_developers:
        score += 20
        rep = "Trusted"
    else:
        score += 10
        rep = "Unknown"

    details["developer_reputation"] = rep

    # =====================================================
    # 2. Install Count (20)
    # =====================================================
    installs = data.get("realInstalls", 0)
    details["installs"] = installs

    if installs >= 10000000:
        score += 20
    elif installs >= 1000000:
        score += 15
    elif installs >= 100000:
        score += 10
    elif installs >= 10000:
        score += 5
        issues.append("Low install count.")
    else:
        issues.append("Very low install count.")

    # =====================================================
    # 3. User Rating (15)
    # =====================================================
    rating = data.get("score", 0)
    details["rating"] = rating

    if rating >= 4.5:
        score += 15
    elif rating >= 4:
        score += 12
    elif rating >= 3:
        score += 8
        issues.append("Average user rating.")
    else:
        score += 3
        issues.append("Poor user rating.")

    # =====================================================
    # 4. Number of Reviews (15)
    # =====================================================
    reviews = data.get("ratings", 0)
    details["reviews"] = reviews

    if reviews >= 1000000:
        score += 15
    elif reviews >= 100000:
        score += 12
    elif reviews >= 10000:
        score += 8
    elif reviews >= 1000:
        score += 5
    else:
        issues.append("Very few reviews available.")

    # =====================================================
    # 5. Update Frequency (15)
    # =====================================================
    updated = data.get("updated")
    details["last_updated"] = updated

    try:
        if updated:
            update_date = datetime.strptime(updated, "%b %d, %Y")
            days = (datetime.now() - update_date).days

            if days <= 180:
                score += 15
            elif days <= 365:
                score += 10
            elif days <= 730:
                score += 5
                issues.append("Application has not been updated recently.")
            else:
                issues.append("Application appears abandoned.")
    except:
        issues.append("Unable to determine update frequency.")

    # =====================================================
    # 6. App Age (10)
    # =====================================================
    released = data.get("released")
    details["released"] = released

    try:
        if released:
            release_date = datetime.strptime(released, "%b %d, %Y")
            years = (datetime.now() - release_date).days / 365

            if years >= 5:
                score += 10
            elif years >= 2:
                score += 7
            elif years >= 1:
                score += 5
            else:
                score += 2
                issues.append("Recently released application.")
    except:
        pass

    # =====================================================
    # 7. Suspicious Description (5)
    # =====================================================
    description = data.get("description", "").lower()

    suspicious_keywords = [
        "hack",
        "mod",
        "unlimited",
        "free money",
        "earn money",
        "cheat",
        "crack",
        "premium unlocked"
    ]

    found = [
        k for k in suspicious_keywords
        if k in description
    ]

    details["suspicious_keywords"] = found

    if not found:
        score += 5
    else:
        issues.append(
            f"Suspicious keywords detected: {', '.join(found)}"
        )

    # =====================================================
    # Risk Level
    # =====================================================
    if score >= 80:
        risk = "Low"
    elif score >= 50:
        risk = "Medium"
    else:
        risk = "High"

    if issues:
        recommendations.append(
            "Review the detected issues before installing the application."
        )

    return {
        "score": score,
        "risk_level": risk,
        "details": details,
        "issues": issues,
        "recommendations": recommendations
    }


# =========================
# PRIVACY ANALYSIS
# =========================
def metadata_privacy(package_name):
    """
    Returns:
    {
        "score": int,
        "risk_level": str,
        "details": {...},
        "issues": [...],
        "recommendations": [...]
    }
    """
    from google_play_scraper import app
    from datetime import datetime
    import requests
    import re


    score = 0
    issues = []
    recommendations = []

    try:
        data = app(package_name, lang="en", country="in")
    except Exception as e:
        return {
            "score": 0,
            "risk_level": "Unknown",
            "details": {},
            "issues": [f"Unable to fetch metadata: {e}"],
            "recommendations": ["Verify package name."]
        }

    details = {}

    # =====================================================
    # 1. Privacy Policy Availability (30)
    # =====================================================
    privacy_policy = data.get("privacyPolicy")
    details["privacy_policy"] = privacy_policy

    if privacy_policy:
        score += 30
    else:
        issues.append("Privacy policy not available.")

    # =====================================================
    # 2. Privacy Policy Analysis (30)
    # =====================================================
    privacy_findings = []

    if privacy_policy:
        try:
            r = requests.get(
                privacy_policy,
                timeout=10,
                headers={"User-Agent": "Mozilla/5.0"}
            )

            text = r.text.lower()

            keywords = {
                "location": "Location Tracking",
                "advertising": "Advertising",
                "third party": "Third Party Sharing",
                "analytics": "Analytics",
                "cookies": "Cookies",
                "personal information": "Personal Information Collection",
                "retain": "Data Retention",
                "sell": "Data Selling"
            }

            count = 0

            for k, v in keywords.items():
                if k in text:
                    privacy_findings.append(v)
                    count += 1

            details["policy_findings"] = privacy_findings

            if count <= 2:
                score += 30
            elif count <= 4:
                score += 20
            elif count <= 6:
                score += 10
            else:
                score += 5
                issues.append(
                    "Privacy policy indicates extensive data collection."
                )

        except:
            issues.append("Unable to analyze privacy policy.")
    else:
        details["policy_findings"] = []

    # =====================================================
    # 3. Developer Transparency (10)
    # =====================================================
    email = data.get("developerEmail")
    website = data.get("developerWebsite")

    details["developer_email"] = email
    details["developer_website"] = website

    if email and website:
        score += 10
    elif email or website:
        score += 5
    else:
        issues.append(
            "Developer contact information is limited."
        )

    # =====================================================
    # 4. Advertising Presence (15)
    # =====================================================
    contains_ads = data.get("containsAds", False)
    details["contains_ads"] = contains_ads

    if contains_ads:
        score += 5
        issues.append(
            "Application contains advertisements."
        )
    else:
        score += 15

    # =====================================================
    # 5. Category Privacy Risk (15)
    # =====================================================
    genre = data.get("genre", "Unknown")
    details["genre"] = genre

    high_risk = [
        "Social",
        "Communication",
        "Dating",
        "Finance",
        "Health & Fitness"
    ]

    medium_risk = [
        "Shopping",
        "Entertainment",
        "Productivity"
    ]

    if genre in high_risk:
        score += 5
        issues.append(
            f"{genre} apps typically collect significant user data."
        )

    elif genre in medium_risk:
        score += 10

    else:
        score += 15

    # =====================================================
    # Risk Level
    # =====================================================
    if score >= 80:
        risk = "Low"
    elif score >= 50:
        risk = "Medium"
    else:
        risk = "High"

    if issues:
        recommendations.append(
            "Review the privacy policy and developer practices carefully."
        )

    return {
        "score": score,
        "risk_level": risk,
        "details": details,
        "issues": issues,
        "recommendations": recommendations
    }

security = metadata_security("com.instagram.android")
privacy = metadata_privacy("com.instagram.android")
for key, value in security.items():
    print(f"{key}: {value}")
for key, value in privacy.items():
    print(f"{key}: {value}")
