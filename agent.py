import random

AGENT_REPLIES = [
    "Why will my account be blocked?",
    "Can you explain the verification process?",
    "Is there another way to fix this?",
    "I am not sure I understand, please help.",
    "What details do you need from me?"
]

def agent_reply():
    return random.choice(AGENT_REPLIES)
