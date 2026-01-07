from app.stemmer import stem_tokens, is_valid_word

def test_stemming_output():
    tokens = ["running", "studies"]
    result = stem_tokens(tokens)

    assert len(result) == 2
    assert "porter" in result[0]
    assert "snowball" in result[0]
    assert "lancaster" in result[0]

def test_invalid_stem_marking():
    tokens = ["better"]
    result = stem_tokens(tokens)

    stem = result[0]["lancaster"]
    expected = is_valid_word(stem)
    assert result[0]["lancaster_valid"] == expected
