def developer(data):
    from google_play_scraper import app
    from datetime import datetime
    import requests
    import re
    score = 0
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
   
    if developer in trusted_developers:
        score += 20
        rep = "Trusted"
    else:
        score += 10
        rep = "Unknown"
    return {
        "score" : score,
        "Developer Score" : f"{score}/20",
        "Reputation" : rep,
        "Developer" : developer
    }

    
def install_count(data):
    from google_play_scraper import app
    from datetime import datetime
    import requests
    import re
    installs = data.get("realInstalls", 0)
    

    if installs >= 10000000:
        score += 20
    elif installs >= 1000000:
        score += 15
    elif installs >= 100000:
        score += 10
    elif installs >= 10000:
        score += 5
        issue =  "Low install count."
    else:
        issue = "Very low install count."
    return {
        "score" : score,
        "Install score" : f"{score}/20",
        "Install count" : installs,
        "Issue" : issue if issue else None
    }

def community_trust(data):
    from google_play_scraper import app
    from datetime import datetime
    import requests
    import re
    score = 0
    reviews = data.get("ratings", 0)
    rating = data.get("score", 0)
    if rating >= 4.5 and reviews >= 10000:
        score += 15
        confidence = "HIGH"
    elif rating >= 4.2 and reviews >= 1000:
        score += 12
        confidence = "MODERATE"

    elif rating >= 4.0 and reviews >= 100:
        score += 10
        confidence = "MODERATE"

    elif rating >= 3.5:
        score += 6
        issue = "Average user satisfaction."
        confidence = "LOW"

    else:
        score += 2
        issue = "Poor user ratings."
        confidence = "LOW"

    return {
        "score" : score,
        "Community score" : f"{score}/15",
        "Community trust" : f"{confidence} Trust",
        "Issue" : issue if issue else None,
        "Note" : """Confidence indicates how reliable the rating is based on the number of user reviews. 
        It does not guarantee the app is secure or private."""
    }

def update_frequency(data):
    from google_play_scraper import app
    from datetime import datetime
    import requests
    import re
    score = 0
    updated = data.get("updated")

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
                issue = "Application has not been updated recently."
            else:
                issue = "Application appears abandoned."
            return {
            "score" : score,
            "Update Frequency Score" : f"{score}/15",
            "Days from last updated" : days,
            "Issue" : issue if issue else None
        }
    except:
        issue = "Unable to determine update frequency."
        return {
            "score" : 0,
            "Update Frequency Score" : "0/15",
            "Issue" : issue
        }

def app_age(data):
    from google_play_scraper import app
    from datetime import datetime
    import requests
    import re
    score = 0
    released = data.get("released")

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
                issue = "Recently released application."
            return {
                "score" : score,
                "Age score" : f"{score}/10",
                "Issue" : issue if issue else None
            }
    except:
        pass

def sus(data):
    from google_play_scraper import app
    from datetime import datetime
    import requests
    import re

    description = data.get("description", "").lower()
    score = 0
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

    if not found:
        score += 10
    else:
        score = 0
        issue = "Suspicious keywords detected"
    return {
        "score" : score,
        "Sus score" : f"{score}/10",
        "Issue" : issue if issue else None,
        "Sus words" : found if found else None
    }

def transparency(data):
    from google_play_scraper import app
    from datetime import datetime
    import requests
    import re
    developer_email = data.get("developerEmail")
    developer_website = data.get("developerWebsite")

    transparency_score = 0
    https_valid = False
    if developer_email:
        transparency_score += 5
    else:
        issue = "Developer email not provided."

    if developer_website:
        if developer_website.startswith("https://"):
            transparency_score += 5
            https_valid = True
        else:
            transparency_score += 2
            issue = "Developer website does not use HTTPS."
            https_valid = False
    else:
        issue = "Developer website not provided."

    return {
        "score" : transparency_score,
        "transparency_score" : f"{transparency_score}/10",
        "https_valid" : https_valid,
        "Issue" : issue if issue else None
    }
            
