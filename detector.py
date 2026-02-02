def is_scam(text: str) -> bool:
    if not text:
        return False

    text = text.lower()

    scam_keywords = [

        # 🏦 Bank / Account Threats
        "bank account",
        "account will be blocked",
        "account blocked",
        "account suspended",
        "account suspension",
        "account freeze",
        "account deactivated",
        "account limited",

        # ⏰ Urgency / Fear Tactics
        "urgent",
        "immediately",
        "verify immediately",
        "action required",
        "last warning",
        "final notice",
        "today only",
        "within 24 hours",
        "failure to comply",

        # 🆔 KYC / Verification Scams
        "kyc",
        "kyc pending",
        "kyc expired",
        "kyc update",
        "verify kyc",
        "re-kyc",
        "document verification",

        # 💳 UPI / Payment Scams
        "upi",
        "upi id",
        "send money",
        "request money",
        "payment failed",
        "payment pending",
        "refund pending",
        "claim refund",
        "test payment",
        "processing fee",

        # 🔗 Phishing / Fake Links
        "click link",
        "verify link",
        "secure link",
        "login now",
        "confirm details",
        "update details",
        "reset password",
        "suspicious activity",
        "unusual activity",

        # 📱 Impersonation / Authority
        "bank support",
        "customer care",
        "technical team",
        "official team",
        "rbi",
        "government",
        "income tax",
        "it department",
        "cyber cell",

        # 🧾 OTP / Credential Theft
        "otp",
        "share otp",
        "do not share otp",
        "pin",
        "atm pin",
        "cvv",
        "password",
        "login credentials"
    ]

    # 🔍 Scam detection logic
    for keyword in scam_keywords:
        if keyword in text:
            return True

    return False
