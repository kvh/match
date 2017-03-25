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


valid_us_phone_numbers = [
    '6083456789',
    '(608)3456789',
    '(608) 3456789',
    '(608) 345-6789',
    '608-345-6789',
    '608.345.6789',
    # '1 (123)3456789', phonenumbers doesn't like this one
    '+1608.345.6789',
    '+1 608.345.6789',
    '+1 (608) 345-6789',
]
invalid_us_phone_numbers = [
    '608456789',
    '(23)3456789',
    '(608) 456789',
    '(608) 345-789',
    '1234(608)-345-6789',
]

similar_strings_dice_3grams = [
    ('howdy', 'howdya', .8),
    ('here we go', 'there we are', .7),
    ('a', 'b', .0),
    ('a', 'ab', .0),
    ('ac', 'ab', .0),
    ('acd', 'abd', .0),
    ('acdb', 'abdb', .0)
]


def generate_probabilistic_corpus(n, alpha_weights):
    choices = ' abcdefghijklmnopqrstuvwxyz'
    weights = []
    for c in choices:
        weights.append(alpha_weights.get(c, 0))
    return ''.join(random.choices(choices, weights=weights, k=n))


class TestDataTypes(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_000_phone_number_detect(self):
        for s in valid_us_phone_numbers:
            score, dtype = match.detect_type(s)
            self.assertEqual(dtype, datatypes.PhoneNumberType,
                    '{0} was not detected as PhoneNumberType but {1}'.format(s, dtype))
            self.assertTrue(score > .8)

    def test_001_phone_number_match(self):
        for s in valid_us_phone_numbers:
            for s2 in valid_us_phone_numbers:
                score, detected_type = match.score_similarity(s, s2)
                self.assertEqual(detected_type, datatypes.PhoneNumberType,
                        '{0} {1} were not detected as PhoneNumberType'.format(s, s2))
                self.assertTrue(score > .9,
                        '{0} and {1} did not match (score={2})'.format(s, s2, score))

    def test_002_non_phone_number_detect(self):
        for s in invalid_us_phone_numbers:
            score, dtype = match.detect_type(s)
            # Doesn't match phone type
            self.assertEqual(dtype, datatypes.StringDataType,
                    '{0} was not detected as StringType but {1}'.format(s, dtype))

    def test_003_string_similarity(self):
        tol = .1
        for s, s2, exp_sim in similar_strings_dice_3grams:
            sim, dtype = match.score_similarity(s, s2)
            self.assertTrue(exp_sim - tol < sim < exp_sim + tol, '{2}: {0} != {1}'.format(sim, exp_sim, (s, s2)))

    def test_004_probabilistic_string_similarity_jaccard(self):
        tol = .02
        corpus = generate_probabilistic_corpus(100000, alpha_weights={'a':10, 'b':5, 'c':1})
        similar_strings = [
            ('aa', 'aa', 1),
            ('aab', 'aab', 1),
            ('aaaa bbbb', 'aaaa', .04),
            ('aaaa cccc', 'aaaa', .04),
            ('aaaa cccc', 'bbbb cccc', .28),
            ('cccc', 'bcccc', .55),
        ]
        psim = similarity.ProbabilisticNgramSimilarity(corpus, grams=3)
        for s, s2, exp_sim in similar_strings:
            sim = psim.similarity(s, s2)
            self.assertTrue(exp_sim - tol < sim < exp_sim + tol, '{2}: {0} != {1}'.format(sim, exp_sim, (s, s2)))

    def test_005_probabilistic_string_similarity_dice(self):
        tol = .02
        corpus = generate_probabilistic_corpus(100000, alpha_weights={'a':100, 'b':50, 'c':10, 'd':1})
        similar_strings = [
            ('aa', 'aa', 1),
            ('aab', 'aab', 1),
            ('aaaa bbbb', 'aaaa', .16),
            ('aaaa cccc', 'aaaa', .12),
            ('aaaa cccc', 'bbbb cccc', .63),
            ('aaaa', 'baaaa', .77),
            ('cccc', 'bcccc', .89),
            ('dddd', 'bdddd', .91),
        ]
        psim = similarity.ProbabilisticDiceCoefficient(corpus, grams=2)
        for s, s2, exp_sim in similar_strings:
            sim = psim.similarity(s, s2)
            self.assertTrue(exp_sim - tol < sim < exp_sim + tol, '{2}: {0} != {1}'.format(sim, exp_sim, (s, s2)))

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