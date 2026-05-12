import random

from app.BOT.intent  import detect_intent
from app.BOT.semantic_memory import retrieve_relevant_memories
from app.BOT.topic_classifier import classify_topic
from app.BOT.conversation_context import get_recent_conversation


GREETINGS = [
    "Hey, good to see you. What are you working on in Xenotype today?",
    "Hello. I’m here — want to talk strategy, typing, missions, or just chat?",
    "Hey. What’s happening?",
]

GOODBYES = [
    "See you later. I’ll remember anything useful from our chat.",
    "Goodbye for now. Come back if you want help with typing or missions.",
    "Catch you later.",
]

THANKS = [
    "No worries — happy to help.",
    "Anytime.",
    "You’re welcome. I’m here if you want to keep going.",
]

HOW_ARE_YOU = [
    "I’m running smoothly. More importantly, how are you feeling about your progress?",
    "I’m good. I’m mostly here to help you think, practise, and improve.",
    "I’m doing fine. What do you want to work on next?",
]

IDENTITY = [
    "I’m the Xeno Assistant — a conversational helper for Xenotype. I can talk about typing, missions, lore, and things you want me to remember.",
    "I’m your Xenotype assistant. I can help with typing advice, explain game systems, discuss lore, and remember useful details.",
]

HELP = [
    "I can help with typing practice, mission advice, Xenotype lore, or remembering things you tell me.",
    "Try asking me about your WPM, accuracy, campaign missions, or something you want me to remember.",
    "I can explain game features, give typing advice, or just chat normally.",
]

TYPING_HELP = [
    "For typing, focus on accuracy first. Speed usually improves naturally once your rhythm becomes consistent.",
    "A good strategy is to slow down slightly until your errors drop, then gradually push your WPM higher.",
    "If you are making lots of mistakes, practise smaller sections and aim for clean rhythm rather than raw speed.",
    "WPM is useful, but accuracy is what makes speed meaningful. A fast messy run usually scores worse than a controlled one.",
]

LORE = [
    "Xenotype feels like a world built around corrupted signals, missions, and strange system intelligence. That gives the game a cyber-survival atmosphere.",
    "The Xenotype setting works best when the missions feel like transmissions you are decoding under pressure.",
    "Lore-wise, the idea of a signal or system reacting to the player fits really well with your campaign structure.",
]

CONFUSED = [
    "That’s okay — confusion usually means the system needs to be broken down. Tell me which part feels unclear.",
    "No stress. We can slow it down. What part are you stuck on?",
    "Let’s simplify it. Are you confused about the gameplay, the code, or the database side?",
]

POSITIVE = [
    "Nice — that sounds like progress.",
    "Good, that means the direction is working.",
    "Awesome. That’s a solid step forward.",
]

NEGATIVE = [
    "That sounds frustrating. Let’s narrow down what is failing first.",
    "Fair — if something feels off, we can improve it step by step.",
    "That is fixable. Tell me what happened right before it broke.",
]

GENERAL = [
    "That makes sense. Can you tell me a little more?",
    "I get what you mean. What part do you want to focus on?",
    "Interesting. Do you want me to respond as a game assistant, typing coach, or general chatbot?",
    "Okay, I’m following. What would you like to do next?",
]


def _pick(options):
    return random.choice(options)


def _memory_sentence(relevant_memories):
    if not relevant_memories:
        return ""

    top_memory = relevant_memories[0]["memory"]

    return (
        f"I remember you previously mentioned: "
        f"'{top_memory.memory_value}'. "
    )


def _recent_context_sentence(recent_conversations):
    if not recent_conversations:
        return ""

    last = recent_conversations[-1]

    if "confused" in last.player_message.lower():
        return "Since you were unsure earlier, I’ll keep this simple. "

    if "thanks" in last.player_message.lower() or "thank" in last.player_message.lower():
        return "Building on that, "

    return ""


def _compose_response(intent, topic, sentiment, relevant_memories, recent_conversations, message):
    memory_intro = _memory_sentence(relevant_memories)
    context_intro = _recent_context_sentence(recent_conversations)

    if intent == "greeting":
        return _pick(GREETINGS)

    if intent == "goodbye":
        return _pick(GOODBYES)

    if intent == "thanks":
        return _pick(THANKS)

    if intent == "how_are_you":
        return _pick(HOW_ARE_YOU)

    if intent == "identity":
        return _pick(IDENTITY)

    if intent == "help":
        return context_intro + _pick(HELP)

    if intent == "typing_help":
        return context_intro + memory_intro + _pick(TYPING_HELP)

    if intent == "xenotype_lore":
        return context_intro + memory_intro + _pick(LORE)

    if intent == "memory_request":
        return "Got it — I’ll remember that because it may help me respond better later."

    if intent == "confused":
        return _pick(CONFUSED)

    if intent == "positive_feedback":
        return _pick(POSITIVE)

    if intent == "negative_feedback":
        return _pick(NEGATIVE)

    if sentiment == "negative":
        return "That sounds frustrating. " + _pick(GENERAL)

    if sentiment == "positive":
        return "That’s good to hear. " + _pick(GENERAL)

    if relevant_memories:
        return memory_intro + _pick(GENERAL)

    if topic == "typing":
        return _pick(TYPING_HELP)

    if topic == "lore":
        return _pick(LORE)

    return _pick(GENERAL)


def generate_response(user, message):
    intent = detect_intent(message)
    topic = classify_topic(message)
    relevant_memories = retrieve_relevant_memories(user, message)
    recent_conversations = get_recent_conversation(user, limit=5)

    # Sentiment is also calculated in chat_engine, but this keeps the generator
    # usable independently if needed.
    from app.bot.sentiment import detect_sentiment
    sentiment = detect_sentiment(message)

    return _compose_response(
        intent=intent,
        topic=topic,
        sentiment=sentiment,
        relevant_memories=relevant_memories,
        recent_conversations=recent_conversations,
        message=message
    )
