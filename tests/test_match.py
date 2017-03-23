#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_match
----------------------------------

Tests for `match` module.
"""


import sys
import unittest

from match import match


valid_us_phone_numbers = [
    '1233456789',
    '(123)3456789',
    '(123) 3456789',
    '(123) 345-6789',
    '123-345-6789',
    '123.345.6789',
    '11233456789',
    '1(123)3456789',
    '1(123) 3456789',
    '1(123) 345-6789',
    '1123-345-6789',
    '1123.345.6789',
    '+1123.345.6789',
    '+1 123.345.6789',
    '+1 (123) 345-6789',
]
invalid_us_phone_numbers = [
    '233456789',
    '(23)3456789',
    '(123) 456789',
    '(123) 345-789',
    '1234(123)-345-6789',
]




class TestDataTypes(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_000_phone_number_detect(self):
        for s in valid_us_phone_numbers:
            score, dtype = match.detect_type(s)
            self.assertEqual(dtype, match.types.PHONE_NUMBER)
            self.assertTrue(score > .8)

    def test_001_phone_number_match(self):
        for s in valid_us_phone_numbers:
            for s2 in valid_us_phone_numbers:
                score, detected_type = match.score(s, s2)
                self.assertEqual(detected_type, match.types.PHONE_NUMBER)
                self.assertTrue(score > .9)
