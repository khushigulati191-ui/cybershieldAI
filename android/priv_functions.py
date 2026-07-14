
def PPAv(data):
    score = 0
    Privacy_Policy_Availability = False
    privacy_policy = data.get("privacyPolicy")
    issue = None
    if privacy_policy:
        Privacy_Policy_Availability = True
        score += 30
    else:
        issue = "Privacy policy not available."
    return {
        "score" : score,
        "PPA score" : f"{score}/30",
        "Privacy_Policy_Availability" : Privacy_Policy_Availability,
        **({"Issue": issue} if issue else {})
    }

def PPAn(data):
    import requests
    privacy_policy = data.get("privacyPolicy")
    privacy_findings = []
    score = 0
    issue = None

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

            if count <= 2:
                score += 30
            elif count <= 4:
                score += 20
            elif count <= 6:
                score += 10
            else:
                score += 5
                issue = "Privacy policy indicates extensive data collection."
                

        except:
            issue = "Unable to analyze privacy policy."
    else:
        issue = "No privacy policy found"
    return {
        "score" : score,
        "Analysis score" : f"{score}/30",
        "Keyword count" : count if count else None,
        "Keywords" : privacy_findings,
        **({"Issue": issue} if issue else {})
    }


def dev_transparency(data):
    import requests
    email = data.get("developerEmail")
    website = data.get("developerWebsite")
    issue = None

    score = 0
    if email and website:
        score += 10
    elif email or website:
        score += 5
    else:
        issue = "Developer contact information is limited."
    return {
        "score" : score,
        "transparency score" : f"{score}/10",
        "email" : email if email else None,
        "website" : website if website else None,
        **({"Issue": issue} if issue else {})
    }
        

def ads(data):
    import requests
    score = 0
    contains_ads = data.get("containsAds", False)
    issue = None

    if contains_ads:
        score += 5
        issue = "Application contains advertisements."
    else:
        score += 15
    return {
        "score" : score,
        "Ads score" : f"{score}/15",
        **({"Issue": issue} if issue else {})
    }


def category_risk(data):
    import requests
    score = 0
    genre = data.get("genre", "Unknown")
    issue = None
    
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
        issue = f"{genre} apps typically collect significant user data."

    elif genre in medium_risk:
        score += 10

    else:
        score += 15
    return {
        "score" : score,
        "category score" : f"{score}/15",
        **({"Issue": issue} if issue else {})
    }


    