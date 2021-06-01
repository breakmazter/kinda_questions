import logging


def top_words(n, text):
    keys = list(set(list(map(lambda word: word if len(word) >= 4 else None, list(set(text.split()))))))
    try:
        keys.remove(None)
    except Exception as e:
        logging.info(f"Catch ---> {e}")

    data = {k: text.split().count(k) for k in keys}
    return ', '.join(sorted(data, key=data.get)[::-1][:n])
