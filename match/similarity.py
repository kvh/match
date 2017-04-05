from collections import Counter
import math

import py_stringmatching as sm

from .utils import clean_to_alphanum, lower_and_strip


similarity_measure_lookup = {

    # Sequence
    'affine': sm.Affine,
    'bag_distance': sm.BagDistance,
    'editex': sm.Editex,
    'hamming_distance': sm.HammingDistance,
    'jaro': sm.Jaro,
    'jaro_winkler': sm.JaroWinkler,
    'levenshtein': sm.Levenshtein,
    'monge_elkan': sm.MongeElkan,
    'needleman_wunsch': sm.NeedlemanWunsch,
    'smith_waterman': sm.SmithWaterman,

    # Phonetic
    'soundex': sm.Soundex,

    # Set-based
    'cosine': sm.Cosine,
    'dice': sm.Dice,
    'generalized_jaccard': sm.GeneralizedJaccard,
    'jaccard': sm.Jaccard,
    'overlap_coefficient': sm.OverlapCoefficient,
    'tversky_index': sm.TverskyIndex,

    # Corpus
    'tfidf': sm.TfIdf,
    'soft_tfidf': sm.SoftTfIdf,
}


tokenizer_lookup = {

    # Character gram tokenizers
    '1gram': sm.QgramTokenizer(qval=1),
    '1grams': sm.QgramTokenizer(qval=1),
    '2grams': sm.QgramTokenizer(qval=2),
    '3grams': sm.QgramTokenizer(qval=3),
    '4grams': sm.QgramTokenizer(qval=4),
    '5grams': sm.QgramTokenizer(qval=5),
    '6grams': sm.QgramTokenizer(qval=6),
    '7grams': sm.QgramTokenizer(qval=7),
    '8grams': sm.QgramTokenizer(qval=8),
    '9grams': sm.QgramTokenizer(qval=9),
    '1gram_set': sm.QgramTokenizer(qval=1, return_set=True),
    '1grams_set': sm.QgramTokenizer(qval=1, return_set=True),
    '2grams_set': sm.QgramTokenizer(qval=2, return_set=True),
    '3grams_set': sm.QgramTokenizer(qval=3, return_set=True),
    '4grams_set': sm.QgramTokenizer(qval=4, return_set=True),
    '5grams_set': sm.QgramTokenizer(qval=5, return_set=True),
    '6grams_set': sm.QgramTokenizer(qval=6, return_set=True),
    '7grams_set': sm.QgramTokenizer(qval=7, return_set=True),
    '8grams_set': sm.QgramTokenizer(qval=8, return_set=True),
    '9grams_set': sm.QgramTokenizer(qval=9, return_set=True),

    # Word tokenizers
    'alphanumeric': sm.AlphanumericTokenizer(),
    'alphanum': sm.AlphanumericTokenizer(),
    'alphabetic': sm.AlphabeticTokenizer(),
    'whitespace': sm.WhitespaceTokenizer(),
    'alphanumeric_set': sm.AlphanumericTokenizer(return_set=True),
    'alphanum_set': sm.AlphanumericTokenizer(return_set=True),
    'alphabetic_set': sm.AlphabeticTokenizer(return_set=True),
    'whitespace_set': sm.WhitespaceTokenizer(return_set=True),
}


cleaner_lookup = {
    'lower_and_strip': lower_and_strip,
    'alphanumeric': clean_to_alphanum,
    'alphanum': clean_to_alphanum,
}


def get_similarity_measure(measure, **kwargs):
    if isinstance(measure, str):
        try:
            return similarity_measure_lookup[measure](**kwargs)
        except KeyError:
            raise KeyError("No such similarity measure {}".format(measure))
    if not (hasattr(measure, 'similarity') or hasattr(measure, 'get_sim_score')):
        raise ValueError("similarity_measure must have a `similarity` or `get_sim_score` callable")
    return measure


def get_tokenizer(tokenizer):
    if isinstance(tokenizer, str):
        try:
            return tokenizer_lookup[tokenizer]
        except KeyError:
            raise KeyError("No such tokenizer {}".format(tokenizer))
    if not hasattr(tokenizer, 'tokenizer'):
        raise ValueError("tokenizer must have a `tokenize` callable")
    return tokenizer


def get_cleaner(cleaner):
    if isinstance(cleaner, str):
        try:
            return cleaner_lookup[cleaner]
        except KeyError:
            raise KeyError("No such cleaner {}".format(cleaner))
    return cleaner




def build_similarity_model(corpus, model_type, tokenizer='3grams',
                           cleaner='alphanum', **model_kwargs):
    pass



class SimilarityModel(object):
    pass




# def make_ngrams(s, grams=3):
#     return [s[i:i + grams] for i in range(len(s) - (grams - 1))]


# class NgramSimilarity(object):

#     def __init__(self, grams=3):
#         self.grams = grams

#     def similarity(self, a, b, grams=None):
#         """
#         """
#         if grams is None:
#             grams = self.grams

#         if not len(a) or not len(b):
#             return 0.0
#         # quick case for true duplicates
#         if a == b:
#             return 1.0
#         # if a != b, and a or b are smaller than 'grams', then they can't possibly match
#         if len(a) < grams or len(b) < grams:
#             return 0.0

#         a_ngram_list = make_ngrams(a, grams)
#         b_ngram_list = make_ngrams(b, grams)

#         return self.ngram_similarity(a_ngram_list, b_ngram_list)

#     def ngram_similarity(self, a_ngram_list, b_ngram_list):
#         """
#         Default to Jaccard similarity
#         """
#         sa = set(a_ngram_list)
#         sb = set(b_ngram_list)
#         return len(sa & sb) / float(len(sa | sb))


# class DiceCoefficientSimilarity(NgramSimilarity):

#     def ngram_similarity(self, a_ngram_list, b_ngram_list):
#         a_ngram_list.sort()
#         b_ngram_list.sort()

#         lena = len(a_ngram_list)
#         lenb = len(b_ngram_list)

#         matches = i = j = 0
#         while (i < lena and j < lenb):
#             if a_ngram_list[i] == b_ngram_list[j]:
#                 matches += 2
#                 i += 1
#                 j += 1
#             elif a_ngram_list[i] < b_ngram_list[j]:
#                 i += 1
#             else:
#                 j += 1

#         score = float(matches) / float(lena + lenb)
#         return score


# class ProbabilisticNgramSimilarity(NgramSimilarity):

#     def __init__(self, corpus, grams=3, smoothing_factor=1):
#         super(ProbabilisticNgramSimilarity, self).__init__(grams=grams)
#         self.smoothing_factor = smoothing_factor
#         self.build_model(corpus)

#     def build_model(self, corpus):
#         tokens = make_ngrams(corpus, self.grams)
#         self.token_counts = Counter(tokens)
#         self.num_tokens = len(tokens)

#     def save(self, name):
#         raise NotImplementedError

#     @classmethod
#     def load(self, name):
#         raise NotImplementedError

#     def get_weight(self, ngram):
#         return math.log(self.num_tokens / float(self.token_counts[ngram] + self.smoothing_factor))

#     def ngram_similarity(self, a_ngram_list, b_ngram_list):
#         """
#         Weighted Jaccard by default
#         """
#         sa = set(a_ngram_list)
#         sb = set(b_ngram_list)
#         intersection_sum = sum([self.get_weight(t) for t in sa & sb])
#         union_sum = sum([self.get_weight(t) for t in sa | sb])
#         return intersection_sum / float(union_sum)


# class ProbabilisticDiceCoefficient(ProbabilisticNgramSimilarity):

#     def ngram_similarity(self, a_ngram_list, b_ngram_list):
#         """
#         Weighted Dice coef
#         """
#         a_ngram_list.sort()
#         b_ngram_list.sort()

#         weights_a = [self.get_weight(t) for t in a_ngram_list]
#         weights_b = [self.get_weight(t) for t in b_ngram_list]

#         lena = len(a_ngram_list)
#         lenb = len(b_ngram_list)

#         matches = i = j = 0
#         while (i < lena and j < lenb):
#             if a_ngram_list[i] == b_ngram_list[j]:
#                 matches += 2 * weights_a[i]
#                 i += 1
#                 j += 1
#             elif a_ngram_list[i] < b_ngram_list[j]:
#                 i += 1
#             else:
#                 j += 1

#         score = matches / float(sum(weights_a) + sum(weights_b))
#         return score
