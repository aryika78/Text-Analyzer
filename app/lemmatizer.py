from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

POS_MAP = {
    "N": "n",
    "V": "v",
    "J": "a",
    "R": "r"
}

lemmatizer = WordNetLemmatizer()

def is_valid_word(word: str):
    return bool(wordnet.synsets(word))


def lemmatize_tokens(tagged_tokens: list[tuple[str, str]]):
    results = []

    for word, pos in tagged_tokens:
        wn_pos = POS_MAP.get(pos[0])
        if wn_pos:
            lemma = lemmatizer.lemmatize(word, pos=wn_pos)
        else:
            lemma = lemmatizer.lemmatize(word)

        results.append({
            "token": word,
            "pos": pos,
            "lemma": lemma,
            "lemma_valid": is_valid_word(lemma)
        })

    return results
