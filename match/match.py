# -*- coding: utf-8 -*-
import logging

from .datatypes import (
    closest_common_type,
    eligible_types,
    get_datatype)


def score_types(s, dtypes):
    scores = []
    for t in dtypes:
        scores.append((t().score_type_match(s), t))
    logging.debug(scores)
    return scores


def detect_type(s):
    scores = score_types(s, eligible_types(s))
    best = max(scores, key=lambda x: x[0])
    return best


def score_similarity(s1, s2):
    score, s1_type = detect_type(s1)
    score, s2_type = detect_type(s2)
    dtype = closest_common_type(s1_type, s2_type)
    return score_similarity_as_type(s1, s2, dtype), dtype


def score_similarity_as_type(s1, s2, dtype):
    score = get_datatype(dtype).score_similarity(s1, s2)
    return score

def parse_as_type(s, dtype, to_object=False):
    return get_datatype(dtype).parse(s, to_object=to_object)
