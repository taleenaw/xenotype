TOPICS = {
    'typing': [
        'keyboard',
        'typing',
        'wpm',
        'accuracy'
    ],

    'gaming': [
        'game',
        'mission',
        'campaign'
    ],

    'lore': [
        'xenotype',
        'signal',
        'ai',
        'world'
    ],

    'social': [
        'friend',
        'chat',
        'talk',
        'people'
    ]
}


def classify_topic(message):

    text = message.lower()

    scores = {}

    for topic, keywords in TOPICS.items():

        score = 0

        for keyword in keywords:
            if keyword in text:
                score += 1

        scores[topic] = score

    best_topic = max(scores, key=scores.get)

    if scores[best_topic] == 0:
        return 'general'

    return best_topic
