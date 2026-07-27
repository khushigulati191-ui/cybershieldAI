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

def check_permissions_transparency(metadata):
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

    return {
        "score" : permission_score,
        "permission_score" : f"{permission_score}/10",
        "status": permission_status,
        "found": found
    }

def analyze_app_age(metadata):
    from datetime import datetime, timezone
    try:
        release_date = metadata.get("releaseDate")

        if not release_date:
            return {
                "score": 0,
                "App Age Score": "0/10",
                "status": "Unknown",
                "app_age_years": None,
                "release_date": None,
                "details": "The app release date is not available in the App Store metadata."
            }

        # Handle ISO format returned by Apple's API
        release_datetime = datetime.fromisoformat(
            release_date.replace("Z", "+00:00")
        )

        current_datetime = datetime.now(timezone.utc)

        # Calculate approximate age in years
        age_days = (current_datetime - release_datetime).days
        age_years = round(age_days / 365.25, 2)

        # Scoring
        if age_years >= 3:
            score = 10
            status = "Established"
            details = (
                f"The app has been available for approximately "
                f"{age_years} years, indicating an established App Store presence."
            )

        elif age_years >= 1:
            score = 7
            status = "Moderately Established"
            details = (
                f"The app has been available for approximately "
                f"{age_years} years."
            )

        elif age_years >= 0.5:
            score = 4
            status = "Relatively New"
            details = (
                f"The app has been available for approximately "
                f"{age_years} years."
            )

        else:
            score = 2
            status = "Very New"
            details = (
                f"The app has been available for less than 6 months."
            )

        return {
            "score": score,
            "App Age Score": f"{score}/10",
            "status": status,
            "app_age_years": age_years,
            "release_date": release_date,
            "details": details
        }

    except Exception as e:
        return {
            "score": 0,
            "App Age Score": "0/10",
            "status": "Error",
            "app_age_years": None,
            "release_date": None,
            "details": f"Unable to analyze app age: {str(e)}"
        }
    
def analyze_account_deletion(metadata):
    try:
        # Apple's App Store metadata may expose this field
        supports_deletion = metadata.get("supportsUserAccountDeletion")

        # Explicitly supports account deletion
        if supports_deletion is True:
            return {
                "score": 15,
                "account deletion score": "15/15",
                "status": "Supported",
                "supports_account_deletion": True,
                "details": (
                    "The app indicates support for user account deletion."
                )
            }

        # Explicitly does not support account deletion
        elif supports_deletion is False:
            return {
                "score": 0,
                "account deletion score": "0/15",
                "status": "Not Supported",
                "supports_account_deletion": False,
                "details": (
                    "The App Store metadata indicates that user account "
                    "deletion is not supported."
                )
            }

        # Metadata does not contain the information
        else:
            return {
                "score": 5,
                "account deletion score": "5/15",
                "status": "Not Specified",
                "supports_account_deletion": None,
                "details": (
                    "The App Store metadata does not clearly specify "
                    "whether users can delete their accounts."
                )
            }

    except Exception as e:
        return {
            "score": 0,
            "account deletion score": "0/15",
            "status": "Error",
            "supports_account_deletion": None,
            "details": (
                f"Unable to analyze account deletion support: {str(e)}"
            )
        }

def analyze_app_popularity(metadata):
    try:
        rating = metadata.get("averageUserRating")
        rating_count = metadata.get("userRatingCount")

        if rating is None or rating_count is None:
            return {
                "score": 0,
                "polularity score": "0/10",
                "status": "Unknown",
                "rating": rating,
                "rating_count": rating_count,
                "details": (
                    "App Store rating or rating count is not available."
                )
            }

        rating = float(rating)
        rating_count = int(rating_count)

        # Scoring
        if rating_count >= 100000 and rating >= 4.0:
            score = 10
            status = "Highly Popular"

        elif rating_count >= 10000 and rating >= 4.0:
            score = 8
            status = "Popular"

        elif rating_count >= 1000 and rating >= 3.5:
            score = 6
            status = "Moderately Popular"

        elif rating_count >= 100:
            score = 4
            status = "Limited Popularity"

        else:
            score = 2
            status = "Low Popularity"

        details = (
            f"The app has an average rating of {rating}/5 "
            f"based on {rating_count:,} ratings."
        )

        return {
            "score": score,
            "popularity score": f"{score}/10",
            "status": status,
            "rating": rating,
            "rating_count": rating_count,
            "details": details
        }

    except Exception as e:
        return {
            "score": 0,
            "popularity score": f"{score}/10",
            "status": "Error",
            "rating": None,
            "rating_count": None,
            "details": (
                f"Unable to analyze App Store popularity: {str(e)}"
            )
        }

