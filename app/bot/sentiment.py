POSITIVE = [
    'good',
    'great',
    'awesome',
    'love',
    'cool',
    'nice',
    'thanks',
    'thank'
]

NEGATIVE = [
    'bad',
    'hate',
    'terrible',
    'awful',
    'annoying',
    'broken',
    'confused'
]


def detect_sentiment(message):
    text = message.lower()

    positive_score = sum(word in text for word in POSITIVE)
    negative_score = sum(word in text for word in NEGATIVE)

    if positive_score > negative_score:
        return 'positive'

    if negative_score > positive_score:
        return 'negative'

    return 'neutral'
