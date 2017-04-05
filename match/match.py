# -*- coding: utf-8 -*-
import logging

from .datatypes import (
    get_closest_common_type,
    eligible_types,
    get_datatype)


"""
Main API
"""

def score_types(s, dtypes):
    scores = []
    for t in dtypes:
        scores.append((get_datatype(t).score_type_match(s), t))
    logging.debug(scores)
    return scores


def detect_type(s):
    scores = score_types(s, eligible_types(s))
    best = max(scores, key=lambda x: x[0])
    return best


def score_similarity(s1, s2, as_type=None, similarity_measure=None, **dtype_kwargs):
    if as_type is None:
        as_type = get_closest_common_type(s1, s2)
    return get_datatype(dtype,
                        similarity_measure=similarity_measure,
                        **dtype_kwargs
               ).score_similarity(s1, s2), as_type


def parse_as(s, dtype, to_object=False, **dtype_kwargs):
    return get_datatype(dtype, **dtype_kwargs).parse(s, to_object=to_object)


def is_exact_match(s1, s2, as_type=None, **dtype_kwargs):
    if as_type is None:
        as_type = get_closest_common_type(s1, s2)
    return get_datatype(as_type, **dtype_kwargs).is_exact_match(s1, s2), as_type


def is_eligible(s, dtype, **dtype_kwargs):
    return get_datatype(dtype, **dtype_kwargs).is_eligible(s)


def build_similarity_model(corpus, model_type='tfidf', **model_kwargs):
    return get_model(model_type, **model_kwargs).fit(corpus)


"""
Convenience functions
"""

def is_phonenumber(s):
    return parse_as(s, 'phonenumber') is not None

def is_email(s):
    return parse_as(s, 'email') is not None

def is_datetime(s):
    return parse_as(s, 'datetime') is not None
