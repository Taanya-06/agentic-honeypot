import random
import re

def agent_reply(user_text: str) -> str:

    if not user_text:
        return _fallback()

    text = user_text.lower()

    # ---------- PHISHING / LINKS ----------
    if _has_link(text) or ("click" in text and "link" in text) or "login" in text:
        return random.choice([
            "Please share the link here.",
            "Is this the official website?",
            "The link is not opening, can you resend it?",
            "Ye link safe hai na?",
            "Can I access this from my phone?"
        ])

    # ---------- UPI / PAYMENT / REFUND ----------
    if any(k in text for k in ["upi", "send money", "payment", "refund", "processing fee", "pay"]):
        return random.choice([
            "Which UPI ID should I use?",
            "How much amount is required?",
            "Can you share the payment details?",
            "UPI payment ka process kya hai?",
            "Is there any reference number for this?"
        ])

    # ---------- KYC / VERIFICATION ----------
    if any(k in text for k in ["kyc", "verify", "verification", "document"]):
        return random.choice([
            "I already completed KYC earlier, why again?",
            "Which document is required now?",
            "Can this be verified through the bank branch?",
            "KYC ke liye exactly kya chahiye?",
            "Is this as per RBI guidelines?"
        ])

    # ---------- BANK / ACCOUNT THREAT ----------
    if any(k in text for k in ["bank", "account", "blocked", "suspended", "freeze", "deactivated"]):
        return random.choice([
            "Why will my bank account be blocked?",
            "Which bank account are you referring to?",
            "I haven’t received any official notice from the bank.",
            "Is there any official message regarding this?",
            "Thoda clearly bataoge account issue kya hai?"
        ])

    # ---------- URGENCY / PRESSURE ----------
    if any(k in text for k in ["urgent", "immediately", "today", "within 24", "final notice"]):
        return random.choice([
            "Why is this so urgent?",
            "Is there any deadline extension possible?",
            "What happens if I don’t do this right now?",
            "Abhi thoda busy hoon, baad me kar sakte hain?"
        ])

    # ---------- OTP / PIN / CREDENTIALS ----------
    if any(k in text for k in ["otp", "pin", "password", "cvv"]):
        return random.choice([
            "Why is OTP required for this?",
            "Can this be done without OTP?",
            "I’m not comfortable sharing OTP.",
            "OTP ke bina verify ho sakta hai kya?"
        ])

    # ---------- FALLBACK ----------
    return _fallback()


def _has_link(text: str) -> bool:
    return bool(re.search(r"https?://|www\.", text))


def _fallback() -> str:
    return random.choice([
        "Can you explain this a bit more?",
        "I didn’t fully understand, what do I need to do?",
        "Please clarify what you mean.",
        "Can you give me more details?",
        "I’m not very familiar with this process.",
        "Let me understand this properly first.",
        "Okay, what should I do next?",
        "I’m listening, please continue.",
        "Thoda clearly samjhaoge?",
        "Mujhe thoda confusion ho raha hai.",
        "Exactly kya karna hai?",
        "Ek minute ruko, main check karta hoon.",
        "Abhi thoda busy hoon.",
        "Iska process kya hai?",
        "Achha, theek hai. Please explain."
    ])
