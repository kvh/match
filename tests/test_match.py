#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
test_match
----------------------------------

Tests for `match` module.
'''

import random
import sys
import unittest

from match import datatypes
from match import match
from match import similarity
from match import utils
from .test_data import datatype_instances



# similar_strings_dice_3grams = [
#     ('howdy', 'howdya', .8),
#     ('here we go', 'there we are', .7),
#     ('a', 'b', .0),
#     ('a', 'ab', .0),
#     ('ac', 'ab', .0),
#     ('acd', 'abd', .0),
#     ('acdb', 'abdb', .0)
# ]


# def generate_probabilistic_corpus(alpha_weights, n=1):
#     s = ''.join(k*w for k, w in alpha_weights.items()) * n
#     random.sample(s, k=len(s))
#     return s


class TestDataTypes(unittest.TestCase):

    DETECTION_SCORE_THRESHOLD = .8

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_detect_type_valid_datatypes(self):
        for dtype, instances in datatype_instances.items():
            for s in instances['valid']:
                score, actual_dtype = match.detect_type(s)
                self.assertEqual(dtype, actual_dtype,
                         "{0}: expected datatype of {1} but got {2}".format(s,
                                                                            dtype,
                                                                            actual_dtype))
                self.assertTrue(score > self.DETECTION_SCORE_THRESHOLD,
                        "{0}: expected score greater than {1} but got {2}".format(s,
                                                                          self.DETECTION_SCORE_THRESHOLD,
                                                                          score))

    def test_parse_type_valid_datatypes(self):
        for dtype, instances in datatype_instances.items():
            for s in instances['valid']:
                parsed = match.parse_as(s, dtype)
                self.assertTrue(parsed is not None,
                         "{0}: failed to parse as type {1}".format(s, dtype))

    def test_parse_type_invalid_datatypes(self):
        for dtype, instances in datatype_instances.items():
            for s in instances['invalid']:
                parsed = match.parse_as(s, dtype)
                self.assertTrue(parsed is None,
                         "{0}: parsed invalid instance as type {1}".format(s, dtype))

    def test_parse_type_equivalent_datatypes(self):
        for dtype, instances in datatype_instances.items():
            canonical = instances['equivalent'][0]
            for s in instances['equivalent']:
                parsed = match.parse_as(s, dtype)
                self.assertEqual(canonical, parsed,
                             "{0}: expected parse of {1} but got {2}".format(s,
                                                                     canonical,
                                                                     parsed))

    def test_is_exact_match_equivalent_datatypes(self):
        for dtype, instances in datatype_instances.items():
            canonical = instances['equivalent'][0]
            for s in instances['equivalent']:
                is_match = match.is_exact_match(s, canonical, dtype)
                self.assertTrue(is_match,
                             "{0}: expected match with {1}".format(s,
                                                             canonical))

# def test_000_phone_number_detect(self):
#         for s in valid_us_phone_numbers:
#             score, dtype = match.detect_type(s)
#             self.assertEqual(dtype, datatypes.PhoneNumberType,
#                     '{0} was not detected as PhoneNumberType but {1}'.format(s, dtype))
#             self.assertTrue(score > .8)

#     def test_001_phone_number_match(self):
#         for s in valid_us_phone_numbers:
#             for s2 in valid_us_phone_numbers:
#                 score, detected_type = match.score_similarity(s, s2)
#                 self.assertEqual(detected_type, datatypes.PhoneNumberType,
#                         '{0} {1} were not detected as PhoneNumberType'.format(s, s2))
#                 self.assertTrue(score > .9,
#                         '{0} and {1} did not match (score={2})'.format(s, s2, score))

#     def test_002_non_phone_number_detect(self):
#         for s in invalid_us_phone_numbers:
#             score, dtype = match.detect_type(s)
#             # Doesn't match phone type
#             self.assertEqual(dtype, datatypes.StringType,
#                     '{0} was not detected as StringType but {1}'.format(s, dtype))

#     def test_003_string_similarity(self):
#         tol = .1
#         for s, s2, exp_sim in similar_strings_dice_3grams:
#             sim, dtype = match.score_similarity(s, s2)
#             self.assertTrue(exp_sim - tol < sim < exp_sim + tol, '{2}: {0} != {1}'.format(sim, exp_sim, (s, s2)))

#     def test_004_probabilistic_string_similarity_jaccard(self):
#         tol = .02
#         corpus = generate_probabilistic_corpus(alpha_weights={'a':10, 'b':5, 'c':1}, n=10000)
#         similar_strings = [
#             ('aa', 'aa', 1),
#             ('aab', 'aab', 1),
#             ('aaaabbbb', 'aaaa', .09),
#             ('aaaacccc', 'aaaa', .02),
#             ('aaaacccc', 'bbbbcccc', .22),
#             ('cccc', 'bcccc', .5),
#         ]
#         psim = similarity.ProbabilisticNgramSimilarity(corpus, grams=3)
#         for s, s2, exp_sim in similar_strings:
#             sim = psim.similarity(s, s2)
#             self.assertTrue(exp_sim - tol < sim < exp_sim + tol, '{2}: {0} != {1}'.format(sim, exp_sim, (s, s2)))

#     def test_005_probabilistic_string_similarity_dice(self):
#         tol = .02
#         corpus = generate_probabilistic_corpus({'a':100, 'b':50, 'c':10, 'd':1}, n=1000)
#         similar_strings = [
#             ('aa', 'aa', 1),
#             ('aab', 'aab', 1),
#             ('aaaabbbb', 'aaaa', .25),
#             ('aaaacccc', 'aaaa', .12),
#             ('aaaacccc', 'bbbbcccc', .43),
#             ('aaaa', 'baaaa', .2),
#             ('cccc', 'bcccc', .77),
#             ('dddd', 'bdddd', .86),
#         ]
#         psim = similarity.ProbabilisticDiceCoefficient(corpus, grams=2)
#         for s, s2, exp_sim in similar_strings:
#             sim = psim.similarity(s, s2)
#             self.assertTrue(exp_sim - tol < sim < exp_sim + tol, '{2}: {0} != {1}'.format(sim, exp_sim, (s, s2)))

    # Waiting on good corpus
    # def test_006_probabilistic_string_similarity_names(self):
    #     tol = .02
    #     corpus = ???
    #     similar_strings = [
    #         ('susan johnson', 'susan johnson', 1),
    #         ('susan johnson', 'susie johnson', .66),
    #         ('susan johnson', 'bob johnson', .59),
    #         ('susan wjorcek', 'susan johnson', .32),
    #         ('susan wjorcek', 'bob wjorcek', .64),
    #         ('susan wjorcek', 'susie wjorcek', .71),
    #     ]
    #     psim = similarity.ProbabilisticDiceCoefficient(corpus, grams=3)
    #     for s, s2, exp_sim in similar_strings:
    #         sim = psim.similarity(s, s2)
    #         self.assertTrue(exp_sim - tol < sim < exp_sim + tol, '{2}: {0} != {1}'.format(sim, exp_sim, (s, s2)))