from app.tokenizer import word_tokens
from app.pos_tagger import pos_tag_tokens

def test_pos_output_structure():
    text = "Apple is buying startups"
    tokens = word_tokens(text)
    result = pos_tag_tokens(tokens)

    assert len(result) > 0
    assert len(result[0]) == 3

def test_proper_noun():
    text = "Apple"
    tokens = word_tokens(text)
    result = pos_tag_tokens(tokens)

    word, tag, _ = result[0]
    assert tag == "NNP"
