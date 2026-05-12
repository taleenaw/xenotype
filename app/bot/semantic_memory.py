from datetime import datetime

from app import db
from app.models import BotMemory
from app.bot.similarity import compute_similarity


SIMILARITY_THRESHOLD = 0.2



def retrieve_relevant_memories(user, message):

    memories = BotMemory.query.filter_by(
        user_id=user.id
    ).all()

    scored = []

    for memory in memories:

        similarity = compute_similarity(
            message,
            memory.memory_value
        )

        if similarity >= SIMILARITY_THRESHOLD:

            memory.last_accessed = datetime.utcnow()

            scored.append({
                'memory': memory,
                'score': similarity
            })

    scored.sort(
        key=lambda x: x['score'],
        reverse=True
    )

    db.session.commit()

    return scored[:5]
