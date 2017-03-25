#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
test_match
----------------------------------

Tests for `match` module.
'''


import sys
import unittest

from match import match
from match import datatypes


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
    ('acdb', 'abdb', .0)k
]


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


