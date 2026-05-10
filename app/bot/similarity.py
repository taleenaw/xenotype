from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


vectorizer = TfidfVectorizer()


def compute_similarity(text_a, text_b):

    vectors = vectorizer.fit_transform([
        text_a,
        text_b
    ])

    similarity = cosine_similarity(vectors[0], vectors[1])

    return float(similarity[0][0])
