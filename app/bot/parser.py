def detect_intent(message: str) -> str:
    message = message.lower().strip()

    if not message:
        return "help"

    help_words = ["help", "commands", "what can i do"]
    status_words = ["status", "stats", "health", "progress"]
    investigate_words = ["look", "search", "inspect", "explore", "investigate", "check"]
    talk_words = ["talk", "speak", "ask", "chat", "message"]
    run_words = ["run", "escape", "leave", "hide", "retreat"]
    fight_words = ["fight", "attack", "challenge", "combat", "strike"]

    if any(word in message for word in help_words):
        return "help"
    if any(word in message for word in status_words):
        return "status"
    if any(word in message for word in investigate_words):
        return "investigate"
    if any(word in message for word in talk_words):
        return "talk"
    if any(word in message for word in run_words):
        return "run"
    if any(word in message for word in fight_words):
        return "fight"

    return "investigate"
