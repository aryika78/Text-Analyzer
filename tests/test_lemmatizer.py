from app.lemmatizer import lemmatize_tokens

def test_verb_lemmatization():
    tokens = [("running", "VBG")]
    result = lemmatize_tokens(tokens)

    assert result[0]["lemma"] == "run"
    assert result[0]["pos"] == "VBG"

def test_noun_lemmatization():
    tokens = [("cars", "NNS")]
    result = lemmatize_tokens(tokens)

    assert result[0]["lemma"] == "car"
    assert result[0]["pos"] == "NNS"

def test_without_pos():
    tokens = [("better", "JJR")]
    result = lemmatize_tokens(tokens)

    assert result[0]["lemma"] == "good"
