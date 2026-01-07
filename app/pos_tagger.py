import nltk

POS_DESCRIPTIONS = {
    "NN": "Noun",
    "NNS": "Plural noun",
    "NNP": "Proper noun",
    "NNPS": "Proper noun (plural)",
    "VB": "Verb (base form)",
    "VBD": "Verb (past tense)",
    "VBG": "Verb (gerund)",
    "VBN": "Verb (past participle)",
    "VBP": "Verb (present)",
    "VBZ": "Verb (3rd person singular)",
    "JJ": "Adjective",
    "JJR": "Adjective (comparative)",
    "JJS": "Adjective (superlative)",
    "RB": "Adverb",
    "RBR": "Adverb (comparative)",
    "RBS": "Adverb (superlative)",
}

def pos_tag_tokens(tokens: list[str]):
    tagged = nltk.pos_tag(tokens)
    result = []

    for word, tag in tagged:
        description = POS_DESCRIPTIONS.get(tag, "Other")
        result.append((word, tag, description))

    return result
