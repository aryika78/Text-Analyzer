from nltk.stem import PorterStemmer, SnowballStemmer, LancasterStemmer
from nltk.corpus import wordnet

porter = PorterStemmer()
snowball = SnowballStemmer("english")
lancaster = LancasterStemmer()

def is_valid_word(word: str):
    return bool(wordnet.synsets(word))


def stem_tokens(tokens: list[str]):
    results = []

    for token in tokens:
        porter_stem = porter.stem(token)
        snowball_stem = snowball.stem(token)
        lancaster_stem = lancaster.stem(token)

        results.append({
            "token": token,
            "porter": porter_stem,
            "snowball": snowball_stem,
            "lancaster": lancaster_stem,
            "porter_valid": is_valid_word(porter_stem),
            "snowball_valid": is_valid_word(snowball_stem),
            "lancaster_valid": is_valid_word(lancaster_stem),
        })

    return results
