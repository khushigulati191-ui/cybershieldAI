def check_developer_verification(metadata):
    from datetime import datetime, timezone
    import requests

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

