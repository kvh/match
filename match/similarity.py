from collections import Counter
import math


def make_ngrams(s, grams=3):
    return [s[i:i + grams] for i in range(len(s) - (grams - 1))]



class NgramSimilarity(object):

    def __init__(self, grams=3):
        self.grams = grams

    def similarity(self, a, b, grams=None):
        """
        """
        if grams is None:
            grams = self.grams

        if not len(a) or not len(b):
            return 0.0
        # quick case for true duplicates
        if a == b:
            return 1.0
        # if a != b, and a or b are smaller than 'grams', then they can't possibly match
        if len(a) < grams or len(b) < grams:
            return 0.0

        a_ngram_list = make_ngrams(a, grams)
        b_ngram_list = make_ngrams(b, grams)

        return self.ngram_similarity(a_ngram_list, b_ngram_list)

    def ngram_similarity(self, a_ngram_list, b_ngram_list):
        """
        Default to Jaccard similarity
        """
        sa = set(a_ngram_list)
        sb = set(b_ngram_list)
        return len(sa & sb) / len(sa | sb)


class DiceCoefficientSimilarity(NgramSimilarity):

    def ngram_similarity(self, a_ngram_list, b_ngram_list):
        a_ngram_list.sort()
        b_ngram_list.sort()

        lena = len(a_ngram_list)
        lenb = len(b_ngram_list)

        matches = i = j = 0
        while (i < lena and j < lenb):
            if a_ngram_list[i] == b_ngram_list[j]:
                matches += 2
                i += 1
                j += 1
            elif a_ngram_list[i] < b_ngram_list[j]:
                i += 1
            else:
                j += 1

        score = float(matches) / float(lena + lenb)
        return score


class ProbabilisticNgramSimilarity(NgramSimilarity):

    def __init__(self, corpus, grams=3, smoothing_factor=1):
        super(ProbabilisticNgramSimilarity, self).__init__(grams=grams)
        self.smoothing_factor = smoothing_factor
        self.build_model(corpus)

    def build_model(self, corpus):
        tokens = make_ngrams(corpus, self.grams)
        self.token_counts = Counter(tokens)
        self.num_tokens = len(tokens)

    def save(self, name):
        raise NotImplementedError

    @classmethod
    def load(self, name):
        raise NotImplementedError

    def get_weight(self, ngram):
        return math.log(self.num_tokens / (self.token_counts[ngram] + self.smoothing_factor))

    def ngram_similarity(self, a_ngram_list, b_ngram_list):
        """
        Weighted Jaccard by default
        """
        sa = set(a_ngram_list)
        sb = set(b_ngram_list)
        intersection_sum = sum([self.get_weight(t) for t in sa & sb])
        union_sum = sum([self.get_weight(t) for t in sa | sb])
        return intersection_sum / union_sum


class ProbabilisticDiceCoefficient(ProbabilisticNgramSimilarity):

    def ngram_similarity(self, a_ngram_list, b_ngram_list):
        """
        Weighted Dice coef
        """
        a_ngram_list.sort()
        b_ngram_list.sort()

        weights_a = [self.get_weight(t) for t in a_ngram_list]
        weights_b = [self.get_weight(t) for t in b_ngram_list]

        lena = len(a_ngram_list)
        lenb = len(b_ngram_list)

        matches = i = j = 0
        while (i < lena and j < lenb):
            if a_ngram_list[i] == b_ngram_list[j]:
                matches += 2 * weights_a[i]
                i += 1
                j += 1
            elif a_ngram_list[i] < b_ngram_list[j]:
                i += 1
            else:
                j += 1

        score = matches / (sum(weights_a) + sum(weights_b))
        return score
