import string

STOP_WORDS = {"is", "the", "a", "an", "of", "to", "in"}

def tokenize(text):
    text = text.lower()
    for punctuation in string.punctuation:
        text = text.replace(punctuation, "")
    words = text.split()
    clean_words = []
    for word in words:
        if word not in STOP_WORDS:
            clean_words.append(word)
    return clean_words