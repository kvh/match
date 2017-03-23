# -*- coding: utf-8 -*-
from .datatypes import DATATYPES, lowest_common_type


def detect_type(s):
    return 0, None


def score(s1, s2):
    s1_type = detect_type(s1)
    s2_type = detect_type(s2)
    dtype = lowest_common_type(s1_type, s2_type)
    return score_for_type(s1, s2, dtype)


def score_for_type(s1, s2, dtype):
    score = dtype.score(s1, s2)
    return score, dtype