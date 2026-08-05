import math


def cosine_similarity(vector1, vector2):

    if vector1 is None or vector2 is None:
        return 0
    dot_product = 0

    for a, b in zip(vector1, vector2):

        dot_product += a * b

    magnitude1 = math.sqrt( sum(x * x for x in vector1))
    magnitude2 = math.sqrt( sum(x * x for x in vector2))
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0
    
    return dot_product / (magnitude1 * magnitude2)