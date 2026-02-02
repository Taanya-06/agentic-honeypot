import random

def agent_reply():
    replies = [
        "Why will my bank account be blocked?",
        "Can you explain the reason for this suspension?",
        "I already completed KYC, why again?",
        "Is there another way to fix this?",
        "I am not sure I understand, please help.",
        "I’m not sure I understood this properly.",
        "Okay, what should I do next?",
        "Can you give me more details?",
        "Please clarify what you mean.",
        "What details do you need from me?",
        "Is there any official notice for this?"
    ]
    return random.choice(replies)

