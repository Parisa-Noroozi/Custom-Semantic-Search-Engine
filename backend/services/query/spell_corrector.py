def similarity(word1, word2):
    count = 0
    for a, b in zip(word1, word2):
        if a == b:
            count += 1
    return count / max(len(word1), len(word2))


def correct_word(query_word, frequency_table ):
    best_word = query_word
    best_score = 0

    for word in frequency_table:
        score = similarity(query_word, word)
        if score > best_score:
            best_score = score
            best_word = word
            
    if best_score < 0.6:
        return None
    return best_word