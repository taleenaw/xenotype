from app import db
from app.models import BotMemory


IMPORTANT_WORDS = [
    'favorite',
    'like',
    'hate',
    'remember',
    'love'
]


def store_memory(user, message):

    words = message.lower().split()

    for word in words:

        if word in IMPORTANT_WORDS:

            memory = BotMemory(
                user_id=user.id,
                memory_key=word,
                memory_value=message
            )

            db.session.add(memory)

    db.session.commit()
