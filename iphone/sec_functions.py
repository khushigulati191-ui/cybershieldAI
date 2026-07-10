def check_developer_verification(metadata):
    
    developer = metadata.get("sellerName", "")
    seller_url = metadata.get("sellerUrl", "")

    if developer and seller_url:
        verification_score = 20
        status = "Verified Developer"
    elif developer:
        verification_score = 10
        status = "Developer information available"
    else:
        verification_score = 0
        status = "Developer information unavailable"

    return {
        "score" : verification_score,
        "verification_score" : f"{verification_score}/20",
        "develper" : developer,
        "seller" : seller_url,
        "status" : status
    }

def check_update_frequency(metadata):
    from datetime import datetime, timezone
    import requests

    release_date = metadata.get("currentVersionReleaseDate")

    update_score = 0
    update_status = "Unknown"

    if release_date:
        try:
            release_date = datetime.fromisoformat(
                release_date.replace("Z", "+00:00")
            )

            today = datetime.now(timezone.utc)
            days = (today - release_date).days

            if days <= 90:
                update_score = 20
                update_status = "Recently Updated"

            elif days <= 180:
                update_score = 15
                update_status = "Moderately Updated"

            elif days <= 365:
                update_score = 10
                update_status = "Old Update"

            else:
                update_score = 0
                update_status = "No Recent Updates"

        except:
            pass
        return {
            "score" : update_score,
            "update_score" : f"{update_score}/20",
            "update_status" : update_status,
            "last updated" : f"{days} days before"
        }
    
def check_developer_website(metadata):
    import requests

    website_score = 0
    website_status = "No Website"
    seller_url = metadata.get("sellerUrl", "")

    if seller_url:
        if seller_url.startswith("https://"):
            website_score = 15
            website_status = "HTTPS Website"

        elif seller_url.startswith("http://"):
            website_score = 5
            website_status = "HTTP Website"
    return {
        "score" : website_score,
        "website_score" : f"{website_score}/15",
        "status": website_status,
        "url": seller_url
    }