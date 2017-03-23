# -*- coding: utf-8 -*-
from .datatypes import datatype_lookup, closest_common_type, eligible_types


def score_types(s, dtypes):
    scores = []
    for t in dtypes:
        scores.append((t.score_type(s), t))
    return scores


def detect_type(s):
    scores = score_types(s, eligible_types(s))
    best = max(scores, key=lambda x:x[0])
    return best


def score(s1, s2):
    score, s1_type = detect_type(s1)
    score, s2_type = detect_type(s2)
    dtype = closest_common_type(s1_type, s2_type)
    return score_for_type(s1, s2, dtype), dtype


def score_for_type(s1, s2, dtype):
    score = dtype.score_match(s1, s2)
    return score
