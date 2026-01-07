import spacy

nlp = spacy.load("en_core_web_sm")

def process_text(text: str):
    return nlp(text)


def extract_entities_from_doc(doc):
    entities = []

    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "label": ent.label_,
            "start": ent.start,
            "end": ent.end
        })

    return entities


def generate_bio_tags_from_doc(doc):
    bio_tags = []

    for token in doc:
        tag = "O"
        for ent in doc.ents:
            if token.i == ent.start:
                tag = f"B-{ent.label_}"
            elif ent.start < token.i < ent.end:
                tag = f"I-{ent.label_}"
        bio_tags.append((token.text, tag))

    return bio_tags
