SCAM_KEYWORDS = [
    "account blocked", "verify", "urgent",
    "upi", "otp", "bank", "suspended"
]

def is_scam(text):
    text = text.lower()
    return any(k in text for k in SCAM_KEYWORDS)
