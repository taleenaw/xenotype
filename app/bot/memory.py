from app import db
from app.models import BotMemory

from app.BOT.topic_classifier import classify_topic
from app.BOT.ner import extract_entities


IMPORTANT_WORDS = [
    'favorite',
    'like',
    'hate',
    'remember',
    'love'
]


MEMORY_THRESHOLD = 2



def calculate_memory_score(message):

    score = 0

    text = message.lower()

    for word in IMPORTANT_WORDS:
        if word in text:
            score += 2

    entities = extract_entities(message)

    score += len(entities)

    if len(message.split()) > 10:
        score += 1

    return score



def store_memory(user, message):

    existing = BotMemory.query.filter_by(
        user_id=user.id,
        memory_value=message
    ).first()

    if existing:
        return

    memory_score = calculate_memory_score(message)

    if memory_score < MEMORY_THRESHOLD:
        return

    topic = classify_topic(message)

    entities = extract_entities(message)

    entity_summary = ', '.join([
        f"{e['text']}:{e['label']}"
        for e in entities
    ])

    memory = BotMemory(
        user_id=user.id,
        memory_key=topic,
        memory_value=message,
        importance=memory_score,
        entity_summary=entity_summary
    )

    db.session.add(memory)
    db.session.commit()
