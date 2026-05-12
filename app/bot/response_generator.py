import random

from app.BOT.semantic_memory import retrieve_relevant_memories
from app.BOT.topic_classifier import classify_topic


GENERAL_RESPONSES = [
    'Interesting.',
    'Tell me more.',
    'I understand.',
    'That sounds important.'
]


TOPIC_RESPONSES = {
    'typing': [
        'Typing rhythm matters more than raw speed.',
        'Accuracy is the foundation of fast typing.'
    ],

    'gaming': [
        'Campaign progression unlocks stronger scenarios.',
        'Mission design affects player engagement heavily.'
    ],

    'lore': [
        'The Xenotype world contains abandoned AI systems and corrupted transmissions.',
        'Signal corruption is central to Xenotype lore.'
    ]
}



def generate_response(user, message):

    topic = classify_topic(message)

    relevant_memories = retrieve_relevant_memories(
        user,
        message
    )

    if relevant_memories:

        top_memory = relevant_memories[0]['memory']

        return (
            f"This reminds me of something you said earlier: "
            f"'{top_memory.memory_value}'"
        )

    if topic in TOPIC_RESPONSES:
        return random.choice(TOPIC_RESPONSES[topic])

    return random.choice(GENERAL_RESPONSES)
