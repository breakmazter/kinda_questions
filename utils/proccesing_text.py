# TODO use in the future
from nltk import word_tokenize


def top_words(n, text):
    keys = list(set(list(map(lambda word: word if len(word) >= 4 else None, list(set(text.split()))))))
    keys.remove(None)

    data = {k: text.split().count(k) for k in keys}
    return ', '.join(sorted(data, key=data.get)[::-1][:n])
