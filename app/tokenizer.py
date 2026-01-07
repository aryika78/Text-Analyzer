import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import tiktoken

def sentence_tokens(text: str):
    return sent_tokenize(text)

def word_tokens(text: str):
    return word_tokenize(text)

def llm_tokens(text: str, model: str = "gpt-4o-mini"):
    enc = tiktoken.encoding_for_model(model)
    tokens = enc.encode(text)
    decoded = [enc.decode([t]) for t in tokens]
    return list(zip(decoded, tokens)), len(tokens)