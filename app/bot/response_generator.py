import random

from app.bot.intent import detect_intent
from app.bot.semantic_memory import retrieve_relevant_memories
from app.bot.topic_classifier import classify_topic
from app.bot.conversation_context import get_recent_conversation
from app.bot.sentiment import detect_sentiment


RESPONSES = {
    "greeting": [
        "Hey. I’m here — want help with typing, missions, campaign mode, or your profile?",
        "Hello. What are we working on today?",
        "Hey, good to see you. Are you practising typing or building something in Xenotype?",
    ],

    "how_are_you": [
        "I’m running smoothly. More importantly, what are you trying to improve right now?",
        "I’m good. I can help with typing, missions, campaign choices, or explaining the app.",
        "Doing fine. Tell me what you want to work on and I’ll help break it down.",
    ],

    "thanks": [
        "No worries — happy to help.",
        "Anytime.",
        "You’re welcome. Keep going, you’re making progress.",
    ],

    "goodbye": [
        "See you later. I’ll be here when you want to practise again.",
        "Catch you later. Good luck with the next mission.",
        "Goodbye for now.",
    ],

    "identity": [
        "I’m the Xeno Assistant — a helper for Xenotype. I can give typing advice, explain features, talk about missions, and remember useful things.",
        "I’m your Xenotype assistant. I’m here to help with gameplay, typing improvement, campaign logic, and general questions.",
    ],

    "typing_coach": [
        "To type better, focus on accuracy before speed. Slow down until you can keep mistakes low, then gradually increase pace.",
        "A strong typing strategy is: aim for clean rhythm, avoid panic typing, and correct patterns that repeatedly cause errors.",
        "If your WPM is low, do short focused runs. If your accuracy is low, slow down and prioritise clean keystrokes.",
        "Try practising difficult words in small chunks. Speed comes from rhythm and confidence, not just pressing keys faster.",
        "For better scores, keep accuracy above 90 percent first. A slightly slower accurate run usually beats a fast messy one.",
    ],

    "typing_help": [
        "Typing improves fastest when you reduce repeated mistakes. Watch which letters or words break your rhythm.",
        "Focus on consistency. Your WPM will rise naturally once your hands stop hesitating.",
        "Try using backspace only when needed. Correcting mistakes is good, but too much correction can break flow.",
    ],

    "game_help": [
        "In Xenotype, you complete typing missions, save runs, earn grades, and compare results on the leaderboard.",
        "Scenarios are typing missions. Campaign mode is more story-driven and lets you choose actions like look, talk, hack, repair, fight, or run.",
        "Your profile tracks your runs and progress. The leaderboard shows strong performances from players.",
    ],

    "xenotype_lore": [
        "Xenotype works best as a corrupted-signal sci-fi world: typing becomes the way you decode, stabilise, or fight the system.",
        "The campaign can feel stronger if each command changes the situation: hacking opens hidden paths, repairing reduces danger, fighting costs health, and talking reveals clues.",
        "The Xenotype setting is about unstable systems, alien signals, damaged AI, and player choices inside a hostile network.",
    ],

    "explain_feature": [
        "I can explain it. Tell me which part you mean: typing missions, campaign mode, leaderboard, profile photos, or chat?",
        "That depends on the feature. Which screen or button are you asking about?",
        "I can break it down step by step. What specific part is confusing?",
    ],

    "bug_report": [
        "That sounds like a bug. First check what page it happens on, what button you pressed, and whether the terminal shows an error.",
        "If something is broken, the best next step is to reproduce it once, check the Flask terminal output, and inspect the route/template involved.",
        "Let’s narrow it down: is it a frontend display issue, a database issue, or a Flask route error?",
    ],

    "memory_request": [
        "Got it — I’ll remember that because it may help me respond better later.",
        "Understood. I’ll treat that as useful context for future replies.",
    ],

    "confused": [
        "No stress. Tell me which part is confusing and I’ll simplify it.",
        "That’s okay. Is the confusing part about the code, the gameplay, or the database?",
        "Let’s slow it down. What was the last thing that made sense?",
    ],

    "positive_feedback": [
        "Nice — that sounds like progress.",
        "Good, that means the direction is working.",
        "Awesome. Keep building on that.",
    ],

    "negative_feedback": [
        "That sounds frustrating. Let’s isolate the problem and fix it one step at a time.",
        "Fair. If it feels wrong, we can improve the logic or the response style.",
        "That is fixable. Tell me what you expected and what actually happened.",
    ],

    "help": [
        "I can help with typing practice, mission strategy, campaign choices, profile issues, chat, or debugging Xenotype.",
        "Try asking: 'help me type better', 'explain campaign mode', 'why is my profile photo broken', or 'how do I improve WPM?'",
    ],

    "general": [
        "I understand. Do you want advice, an explanation, or help fixing something?",
        "That makes sense. What part should we focus on next?",
        "I’m following. Tell me a little more so I can give a better answer.",
    ],
}


def _pick(intent):
    return random.choice(RESPONSES.get(intent, RESPONSES["general"]))


def _memory_sentence(relevant_memories):
    if not relevant_memories:
        return ""

    memory = relevant_memories[0]["memory"]

    return f"I remember you previously mentioned: '{memory.memory_value}'. "


def _recent_context_sentence(recent_conversations):
    if not recent_conversations:
        return ""

    last = recent_conversations[-1].player_message.lower()

    if "confused" in last or "don't understand" in last:
        return "Since you were unsure earlier, I’ll keep this simple. "

    if "typing" in last or "wpm" in last or "accuracy" in last:
        return "Continuing from typing practice, "

    if "bug" in last or "broken" in last or "error" in last:
        return "Continuing from that issue, "

    return ""


def generate_response(user, message):
    intent = detect_intent(message)
    topic = classify_topic(message)
    sentiment = detect_sentiment(message)

    relevant_memories = retrieve_relevant_memories(user, message)
    recent_conversations = get_recent_conversation(user, limit=5)

    context = _recent_context_sentence(recent_conversations)
    memory = _memory_sentence(relevant_memories)

    if intent in RESPONSES:
        return context + memory + _pick(intent)

    if topic == "typing":
        return context + memory + _pick("typing_coach")

    if topic == "lore":
        return context + memory + _pick("xenotype_lore")

    if sentiment == "negative":
        return context + _pick("negative_feedback")

    if sentiment == "positive":
        return context + _pick("positive_feedback")

    if relevant_memories:
        return memory + _pick("general")

    return _pick("general")
