from datetime import datetime, timezone
import requests


def ios_security_analysis(apple_id):
    """
    metadata = dictionary returned from Apple lookup API
    """

    score = 0
    results = {}
    lookup_url = f"https://itunes.apple.com/lookup?id={apple_id}"
    metadata = requests.get(lookup_url).json()["results"][0]

    # print(metadata)
    # ======================
    # 1. Developer Verification (20)
    # ======================

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

    score += verification_score

    results["developer_verification"] = {
        "status": status,
        "score": verification_score
    }

    # ======================
    # 2. Update Frequency (20)
    # ======================

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

    score += update_score

    results["update_frequency"] = {
        "status": update_status,
        "score": update_score
    }

    # ======================
    # 3. Developer Website HTTPS (15)
    # ======================

    website_score = 0
    website_status = "No Website"

    if seller_url:
        if seller_url.startswith("https://"):
            website_score = 15
            website_status = "HTTPS Website"

        elif seller_url.startswith("http://"):
            website_score = 5
            website_status = "HTTP Website"

    score += website_score

    results["developer_website"] = {
        "status": website_status,
        "score": website_score,
        "url": seller_url
    }

    # ======================
    # 4. Age Rating (10)
    # ======================

    rating = metadata.get("contentAdvisoryRating", "")

    if rating in ["4+", "9+"]:
        age_score = 10
    elif rating == "12+":
        age_score = 7
    else:
        age_score = 5

    score += age_score

    results["age_rating"] = {
        "rating": rating,
        "score": age_score
    }

    # ======================
    # 5. Permissions Transparency (10)
    # ======================

    description = metadata.get("description", "").lower()

    permission_words = [
        "camera",
        "microphone",
        "location",
        "contacts",
        "photos",
        "notifications"
    ]

    found = []

    for word in permission_words:
        if word in description:
            found.append(word)

    if len(found) >= 3:
        permission_score = 10
        permission_status = "Permissions clearly mentioned"

    elif len(found) > 0:
        permission_score = 5
        permission_status = "Some permissions mentioned"

    else:
        permission_score = 0
        permission_status = "No permissions mentioned"

    score += permission_score

    results["permissions"] = {
        "status": permission_status,
        "found": found,
        "score": permission_score
    }

    # ======================
    # 6. App Reputation (25)
    # ======================

    rating = metadata.get("averageUserRating", 0)
    rating_count = metadata.get("userRatingCount", 0)

    reputation_score = 0

    if rating >= 4.5 and rating_count >= 100000:
        reputation_score = 25
        reputation_status = "Excellent Reputation"

    elif rating >= 4.0 and rating_count >= 10000:
        reputation_score = 20
        reputation_status = "Good Reputation"

    elif rating >= 3.5:
        reputation_score = 15
        reputation_status = "Average Reputation"

    else:
        reputation_score = 5
        reputation_status = "Poor Reputation"

    score += reputation_score

    results["app_reputation"] = {
        "rating": rating,
        "rating_count": rating_count,
        "status": reputation_status,
        "score": reputation_score
    }

    # ======================
    # Final Risk Level
    # ======================

    if score >= 80:
        risk = "Low Risk"

    elif score >= 60:
        risk = "Medium Risk"

    else:
        risk = "High Risk"

    results["total_score"] = score
    results["risk_level"] = risk

    return results

ans = ios_security_analysis(544007664)

print(ans)