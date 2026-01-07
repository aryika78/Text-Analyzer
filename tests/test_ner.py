from app.ner import (
    process_text,
    extract_entities_from_doc,
    generate_bio_tags_from_doc
)

def test_ner_detects_entity():
    doc = process_text("Apple is in California")
    entities = extract_entities_from_doc(doc)

    assert any(e["label"] in {"ORG", "GPE"} for e in entities)


def test_bio_tags_present():
    doc = process_text("Apple is in California")
    tags = generate_bio_tags_from_doc(doc)

    assert any(tag.startswith("B-") for _, tag in tags)
