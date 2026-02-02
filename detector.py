import re

def is_scam(text: str) -> bool:
    if not text:
        return False

    text = text.lower()
    score = 0

    # Phishing links (very strong signal)
    if re.search(r"https?://|www\.", text):
        score += 3

    # Bank / account related
    if any(k in text for k in [
        "bank", "account", "blocked", "suspended", "freeze", "deactivated"
    ]):
        score += 2

    # Pressure / urgency (VERY IMPORTANT)
    if any(k in text for k in [
        "urgent",
        "immediately",
        "final notice",
        "action required",
        "within 24",
        "today",
        "last warning"
    ]):
        score += 2

    # Verification / KYC
    if any(k in text for k in [
        "verify",
        "verification",
        "kyc",
        "document"
    ]):
        score += 1

    # Payment / UPI
    if any(k in text for k in [
        "upi",
        "send money",
        "payment",
        "refund",
        "processing fee"
    ]):
        score += 2

    # Credentials
    if any(k in text for k in [
        "otp",
        "pin",
        "password",
        "cvv"
    ]):
        score += 3

    return score >= 2
