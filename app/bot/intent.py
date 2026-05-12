import re


INTENT_PATTERNS = {
    "greeting": [
        r"\bhi\b",
        r"\bhello\b",
        r"\bhey\b",
        r"\bgday\b",
        r"\bgood morning\b",
        r"\bgood afternoon\b",
        r"\bgood evening\b",
    ],

    "goodbye": [
        r"\bbye\b",
        r"\bgoodbye\b",
        r"\bsee you\b",
        r"\btalk later\b",
    ],

    "thanks": [
        r"\bthanks\b",
        r"\bthank you\b",
        r"\bcheers\b",
        r"\bappreciate it\b",
    ],

    "how_are_you": [
        r"\bhow are you\b",
        r"\bhow's it going\b",
        r"\bhow are things\b",
        r"\bwhat's up\b",
    ],

    "identity": [
        r"\bwho are you\b",
        r"\bwhat are you\b",
        r"\bwhat do you do\b",
    ],

    "help": [
        r"\bhelp\b",
        r"\bi need help\b",
        r"\bcan you help\b",
        r"\bwhat should i do\b",
    ],

    "typing_help": [
        r"\btyping\b",
        r"\bwpm\b",
        r"\baccuracy\b",
        r"\bkeyboard\b",
        r"\bspeed\b",
        r"\bmistakes\b",
        r"\berrors\b",
        r"\bpractice\b",
    ],

    "xenotype_lore": [
        r"\bxenotype\b",
        r"\blore\b",
        r"\bstory\b",
        r"\bsignal\b",
        r"\bworld\b",
        r"\bmission\b",
        r"\bcampaign\b",
    ],

    "memory_request": [
        r"\bremember\b",
        r"\bdon't forget\b",
        r"\bkeep in mind\b",
        r"\bmy favourite\b",
        r"\bmy favorite\b",
        r"\bi like\b",
        r"\bi love\b",
        r"\bi hate\b",
    ],

    "confused": [
        r"\bi'm confused\b",
        r"\bi am confused\b",
        r"\bdon't understand\b",
        r"\bnot sure\b",
        r"\bwhat does this mean\b",
    ],

    "positive_feedback": [
        r"\bcool\b",
        r"\bnice\b",
        r"\bawesome\b",
        r"\bgreat\b",
        r"\blove this\b",
        r"\bthat works\b",
    ],

    "negative_feedback": [
        r"\bthis sucks\b",
        r"\bbad\b",
        r"\bnot good\b",
        r"\bdoesn't work\b",
        r"\bbroken\b",
        r"\bannoying\b",
    ],
}


def detect_intent(message):
    text = message.lower().strip()

    scores = {}

    for intent, patterns in INTENT_PATTERNS.items():
        score = 0

        for pattern in patterns:
            if re.search(pattern, text):
                score += 1

        scores[intent] = score

    best_intent = max(scores, key=scores.get)

    if scores[best_intent] == 0:
        return "general"

    return best_intent
