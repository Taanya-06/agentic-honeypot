import re

def extract(text: str) -> dict:
    upi = re.findall(r'\b[\w.-]+@[\w.-]+\b', text)
    links = re.findall(r'https?://\S+', text)
    accounts = re.findall(r'\b\d{9,18}\b', text)

    return {
        "upiIds": upi,
        "phishingLinks": links,
        "bankAccounts": accounts,
        "phoneNumbers": [],
        "suspiciousKeywords": []
    }

