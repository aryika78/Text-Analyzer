import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import tiktoken

def sentence_tokens(text: str):
    return sent_tokenize(text)

def word_tokens(text: str):
    return word_tokenize(text)

def llm_tokens(text: str, model: str = "gpt-4o-mini"):
    # Use the exact tokenizer used by GPT-4 / GPT-4o family
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(text)
    decoded = [enc.decode([t]) for t in tokens]
    return list(zip(decoded, tokens)), len(tokens)
