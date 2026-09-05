

#SECURITY CHECKS

def https_check(final_url):
    global sec_score
    score = 0
    if final_url.startswith("https://"):
        score+=10
        https_score = "10/10"
        https_enabled = True
        redirect = True
    elif final_url.startswith("http://"):
        score+=5
        https_score = "5/10"
        https_enabled = False
        redirect = False
    else:
        score+=0
        https_score = "0/10"
        https_enabled = False
        redirect = False
    return {
        "score" : score,
        "https_score" : https_score,
        "https_enabled" : https_enabled,
        "redirect" : redirect
    }


def ssl_check(final_url):
    import ssl
    import socket,certifi
    from urllib.parse import urlparse
    score = 0
    try:
        hostname = urlparse(final_url).netloc

        context = ssl._create_unverified_context()

        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert_bin = ssock.getpeercert(binary_form=True)

        score+=5                                      #cerificate is present
        from cryptography import x509
        from cryptography.hazmat.backends import default_backend

        cert_obj = x509.load_der_x509_certificate(
            cert_bin,
            default_backend()
        )

        expiry_date = cert_obj.not_valid_after_utc
        issuer = cert_obj.issuer
        subject = cert_obj.subject
        formatted_expiry = expiry_date.strftime("%Y-%m-%d")
        from datetime import datetime, timezone

        
        current_date = datetime.now(timezone.utc)

        if expiry_date > current_date:
            score+=3                                  #certificate is not expired
            ssl_expired = False
        else:
            score+=0                                  #certificate is expired
            ssl_expired = True

        days_left = (expiry_date - current_date).days
        if days_left > 90:
            status = "Healthy"
        elif days_left > 30:
            status = "Warning"
        elif days_left > 0:
            status = "Expiring Soon"
        else:
            status = "Expired"

        try:
            context = ssl.create_default_context(cafile=certifi.where())

            with socket.create_connection((hostname, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=hostname):
                    ssl_trusted = True
            score+=5    #certificate is trusted

        except ssl.SSLCertVerificationError as e:
            print("TRUST ERROR:", e)
            ssl_trusted = False
            score+=0    #certificate is not trusted
    
        
        if subject == issuer:
            score+=0        #self-signed
            ssl_self_signed = True
        else:
            score+=2        # not self-signed
            ssl_self_signed = False


        return {
            "score":score,
            "ssl_score" : f"{score}/15",
            "ssl_present" : True,
            "ssl_trusted" : ssl_trusted,
            "ssl_expired" : ssl_expired,
            "ssl_self_signed" : ssl_self_signed,
            "ssl_issuer" : issuer,
            "ssl_expiry_date" : formatted_expiry,
            "days_until_expiry" : days_left,
            "status" : status
        }

    except Exception as e:
        print(e)
        return {
            "score" : 0,
            "ssl_score" : f"{score}/15",
            "ssl_present" : False
        }
    
import whois
from urllib.parse import urlparse
from datetime import datetime


def domain_check(url):
    try:
        # Extract domain
        domain = urlparse(url).netloc

        # Remove port if present
        domain = domain.split(":")[0]

        # Remove www.
        if domain.startswith("www."):
            domain = domain[4:]

        try:
            w = whois.whois(domain)
        except Exception as e:
            return {
                "score": 0,
                "domain_score": "0/10",
                "domain": domain,
                "status": "WHOIS lookup unavailable",
                "error": str(e),
                "registrar": "Unknown",
                "creation_date": "Unknown",
                "expiration_date": "Unknown",
                "domain_age_days": None
            }

        # Safely handle list/datetime values
        creation_date = w.creation_date
        expiration_date = w.expiration_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0] if creation_date else None

        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0] if expiration_date else None

        # Calculate domain age
        domain_age_days = None

        if isinstance(creation_date, datetime):
            domain_age_days = (datetime.now() - creation_date).days

        return {
            "score": 10,
            "domain_score": "10/10",
            "domain": domain,
            "status": "WHOIS data available",
            "registrar": w.registrar or "Unknown",
            "creation_date": str(creation_date) if creation_date else "Unknown",
            "expiration_date": str(expiration_date) if expiration_date else "Unknown",
            "domain_age_days": domain_age_days
        }

    except Exception as e:
        return {
            "score": 0,
            "domain_score": "0/10",
            "domain": "Unknown",
            "status": "Domain analysis failed",
            "error": str(e),
            "registrar": "Unknown",
            "creation_date": "Unknown",
            "expiration_date": "Unknown",
            "domain_age_days": None
        }

def security_headers_check(final_url):
    score = 0
    import requests
    try:
        response = requests.get(final_url, timeout=10)
        headers = response.headers
        csp = headers.get("Content-Security-Policy", "Missing")
        hsts = headers.get("Strict-Transport-Security", "Missing")
        xfo = headers.get("X-Frame-Options", "Missing")
        xcto = headers.get("X-Content-Type-Options", "Missing")
        referrer = headers.get("Referrer-Policy", "Missing")
        permissions = headers.get("Permissions-Policy", "Missing")
        if csp != "Missing": 
            csp = csp.lower()
            risky = [
                "*",
                "'unsafe-inline'",
                "'unsafe-eval'"
            ]
            secure = [
                "default-src 'self'",
                "object-src 'none'",
                "frame-ancestors",
                "base-uri"
            ]
            weak_count = sum(1 for item in risky if item in csp)
            strong_count = sum(1 for item in secure if item in csp)
            if weak_count > 0:
                score+=2
                csp_status = "weak"
            elif strong_count >= 3:
                score+=7
                csp_status = "strong"
            else:
                score+=4
                csp_status = "moderate"
        if hsts != "Missing":
            score += 4
        if xfo != "Missing":
            score += 3
        if xcto != "Missing":
            score += 2
        if referrer != "Missing":
            score += 2
        if permissions != "Missing":
            score += 2
        return {
            "score" : score,
            "security_header_score" : f"{score}/20",
            "Content-Security-Policy": csp,
            "Strict-Transport-Security": hsts,
            "X-Frame-Options": xfo,
            "X-Content-Type-Options": xcto,
            "Referrer-Policy": referrer,
            "Permissions-Policy": permissions
        }
    except Exception as e:
        return {
            "score" : 0,
            "security_header_score" : f"{score}/20",
            "error": str(e)
        }

def indicators_check(final_url,url):
    score = 15
    import ipaddress
    from urllib.parse import urlparse

    domain = urlparse(url).hostname
    try:
        ipaddress.ip_address(domain)
        score-=3
        URL_uses_an_IP = True
    except:
        URL_uses_an_IP = False
    if len(final_url) > 100:
        score-=1
        length = "long"
    else:
        length = "Normal"
    parts = domain.split(".")
    if len(parts) > 3:
        score-=1
        subdomains = "many"
    else:
        subdomains = "not many"
    if "@" in final_url:
       score-=2
       symbol = "@ True"
    else:
       symbol = "@ False"
    path = final_url.split("://",1)[1]
    if "//" in path:
        score-=1
        Multiple_slashes = "// True" 
    else:
        Multiple_slashes = "// False" 
    if domain.count("-") >= 2:
        score-=1
        Many_hyphens = True
    else:
        Many_hyphens = False
    keywords = [
    "login","verify","secure","update","bank","gift","bonus","account","signin", "confirm"
    ]
    url_lower = final_url.lower()
    for k in keywords:
        if k in url_lower:
            score-=1
            sus_keywords = True
            break
        else:
            sus_keywords = False
    digits = sum(c.isdigit() for c in domain)
    if digits >= 5:
        score-=1
        Many_digits = True
    else:
        Many_digits = False
    if domain.startswith("xn--"):
        score-=1
        punycode = True
    else:
        punycode = False
    shorteners = {"bit.ly","tinyurl.com", "t.co", "goo.gl", "ow.ly","buff.ly","is.gd","cutt.ly","rb.gy","shorturl.at"
    }
    if domain in shorteners:
        score-=1
        shorteners = True
    else:
        shorteners = False
    suspicious = {"xyz","top","click","work","gq","tk","cf","ml"
    }
    tld = domain.split(".")[-1]
    if tld in suspicious:
        score-=1
        sus_tld = True
    else:
        sus_tld = False

    return {
        "score" : score,
        "indicators_score" : f"{score}/15",
        "URL_uses_an_IP" : URL_uses_an_IP,
        "length" : length,
        "subdomains" : subdomains,
        "symbol" : symbol,
        "Multiple_slashes" : Multiple_slashes,
        "Many_hyphens" : Many_hyphens,
        "sus_keywords" : sus_keywords,
        "Many_digits" : Many_digits, "punycode" : punycode, "shorteners" : shorteners, "sus_tld" : sus_tld
    }

def DNS_check(final_url):
    import dns.resolver
    from urllib.parse import urlparse
    score = 0

    domain = urlparse(final_url).netloc
    if domain.startswith("www."):
        domain = domain[4:]

    try:
        # Get A records
        answers = dns.resolver.resolve(domain, "A")
        ips = [record.address for record in answers]

        # DNS resolves
        DNS_resolves = True
        score += 3

        # Store IPs
        IP_Addresses = ips

        # Multiple records
        if len(ips) > 1:
            Multiple_DNS_records = True
            score += 2
        else:
            Multiple_DNS_records = False

    except Exception:
        # DNS resolution failed
        DNS_resolves = False
        Multiple_DNS_records = "not applicable"
        IP_Addresses = "not applicable"
        
    return {
        "score" : score,
        "DNS_score" : f"{score}/5",
        "DNS_resolves" : DNS_resolves,
        "Multiple_DNS_records" : Multiple_DNS_records,
        "IP_Addresses" : IP_Addresses
    }
    
        
