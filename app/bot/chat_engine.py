from app.BOT.response_generator import generate_response
from app.BOT.memory import store_memory
from app.BOT.sentiment import detect_sentiment
from app.BOT.topic_classifier import classify_topic


class BotEngine:

    def process_message(self, user, message):

        sentiment = detect_sentiment(message)

        topic = classify_topic(message)

        store_memory(user, message)

        response = generate_response(user, message)

        return {
            'response': response,
            'sentiment': sentiment,
            'topic': topic
        }
