from app.tokenizer import sentence_tokens, word_tokens, llm_tokens

def test_sentence_tokenization():
    text = "Hello world. How are you?"
    assert len(sentence_tokens(text)) == 2

def test_word_tokenization():
    text = "Hello world!"
    assert "Hello" in word_tokens(text)

def test_llm_tokens():
    text = "Hello"
    tokens, count = llm_tokens(text)
    assert count > 0
