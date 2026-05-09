from app.bot.response_generator import generate_response
from app.bot.memory import store_memory
from app.bot.sentiment import detect_sentiment


class BotEngine:

    def process_message(self, user, message):

        sentiment = detect_sentiment(message)

        store_memory(user, message)

        response = generate_response(user, message)

        return {
            'response': response,
            'sentiment': sentiment
        }
