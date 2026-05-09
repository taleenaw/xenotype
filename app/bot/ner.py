import spacy

try:

    nlp = spacy.load('en_core_web_sm')

except OSError:

    nlp = spacy.blank('en')

def extract_entities(text):

    doc = nlp(text)

    entities = []

    for ent in doc.ents:

        entities.append({

            'text': ent.text,

            'label': ent.label_

        })

    return entities
