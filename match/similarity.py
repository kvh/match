

def make_ngrams(s, grams=3):
    return [s[i:i+grams] for i in range(len(s)-(grams-1))]


def dice_coefficient(a, b, grams=3):
    """
    Dice coefficient for character ngrams.
    """
    if not len(a) or not len(b): return 0.0
    """ quick case for true duplicates """
    if a == b: return 1.0
    # if a != b, and a or b are smaller than 'grams', then they can't possibly match
    if len(a) < grams or len(b) < grams: return 0.0

    a_bigram_list = make_ngrams(a, grams)
    b_bigram_list = make_ngrams(b, grams)

    lena = len(a_bigram_list)
    lenb = len(b_bigram_list)

    a_bigram_list.sort()
    b_bigram_list.sort()
    # initialize match counters
    matches = i = j = 0
    while (i < lena and j < lenb):
        if a_bigram_list[i] == b_bigram_list[j]:
            matches += 2
            i += 1
            j += 1
        elif a_bigram_list[i] < b_bigram_list[j]:
            i += 1
        else:
            j += 1

    score = float(matches) / float(lena + lenb)
    return score
