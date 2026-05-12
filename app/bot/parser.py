def detect_intent(message: str) -> str:
    message = message.lower().strip()

    if not message:
        return "help"

    intent_words = {
        "help": [
            "help",
            "commands",
            "what can i do",
            "options",
            "actions",
        ],
        "status": [
            "status",
            "stats",
            "health",
            "progress",
            "condition",
        ],
        "investigate": [
            "look",
            "search",
            "inspect",
            "explore",
            "investigate",
            "check",
            "scan",
            "examine",
        ],
        "talk": [
            "talk",
            "speak",
            "ask",
            "chat",
            "message",
            "question",
            "negotiate",
        ],
        "run": [
            "run",
            "escape",
            "leave",
            "hide",
            "retreat",
            "evade",
            "fallback",
        ],
        "fight": [
            "fight",
            "attack",
            "challenge",
            "combat",
            "strike",
            "defend",
            "shoot",
        ],
        "hack": [
            "hack",
            "decode",
            "decrypt",
            "bypass",
            "override",
            "breach",
            "interface",
        ],
        "repair": [
            "repair",
            "fix",
            "stabilise",
            "stabilize",
            "restore",
            "patch",
            "reboot",
        ],
        "use": [
            "use",
            "activate",
            "insert",
            "open",
            "unlock",
            "deploy",
            "trigger",
        ],
    }

    for intent, words in intent_words.items():
        if any(word in message for word in words):
            return intent

    return "investigate"
