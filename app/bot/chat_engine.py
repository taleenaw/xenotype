from app.bot.response_generator import generate_response
from app.bot.memory import store_memory
from app.bot.sentiment import detect_sentiment
from app.bot.topic_classifier import classify_topic
from app.bot.intent import detect_intent

class BotEngine:

    def process_message(self, user, message):

        sentiment = detect_sentiment(message)

        topic = classify_topic(message)

        intent = detect_intent(message)

        store_memory(user, message)

        response = generate_response(user, message)

        return {
            'response': response,
            'sentiment': sentiment,
            'topic': topic
            'intent': intent
        }
