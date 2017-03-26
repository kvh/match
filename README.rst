===============================
Match
===============================


.. image:: https://img.shields.io/pypi/v/match.svg
        :target: https://pypi.python.org/pypi/match

.. image:: https://img.shields.io/travis/kvh/match.svg
        :target: https://travis-ci.org/kvh/match

.. image:: https://readthedocs.org/projects/match/badge/?version=latest
        :target: https://match.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/kvh/match/shield.svg
     :target: https://pyup.io/repos/github/kvh/match/
     :alt: Updates


Probabilistic Entity Matching


* Free software: MIT license
* Documentation: https://match.readthedocs.io.


Installation
--------

* TODO

Usage
--------

Basic entity detection and matching for built-in types.

.. code:: python

    >>> import match
    >>> match.detect_type('608-555-5555')
    (1, PhoneNumberType)
    >>> match.detect_type('joe.van.gogh@example.com')
    (1, EmailType)
    >>> match.detect_type('John R. Smith')
    (.95, FullNameType)
    >>> match.detect_type('Hi, how are you?')
    (1, StringType)

    >>> match.score_similarity('Jonathon R. Smith', 'john r smith')
    (.92, FullNameType)
    >>> match.score_similarity('123 easy st, NY, NY', '123 Easy Street, New York City')
    (.98, AddressType)
    >>> match.score_similarity('Hi, how are you Joe?', 'hi how are you doing joe?')
    (.81, StringType)
    >>> match.score_similarity_as_type('608-555-5555', '608-555-5554', 'phonenumber')
    .0
    >>> match.score_similarity_as_type('608-555-5555', '608-555-5554', 'string')
    .9

    >>> match.parse('608-555-5555')
    ('+1 608 555 5555', PhoneNumberType)
    >>> match.parse(' march 3rd, 1997', to_object=True)
    (datetime.datetime(1997, 3, 3), DateTimeType)
    >>> match.parse_as_type(' march 3rd, 1997', 'email')
    None


Probabilistic matching, based on frequencies in a given corpus.

.. code:: python

    >>> from match import similarities
    >>> import random
    >>> corpus = random.sample('a'*10000 + ' '*10000 + 'b'*1000 + 'c'*100 + 'd'*10, k=21110)
    >>> psim = similarities.ProbabilisticNgramSimilarity(corpus, grams=2)
    >>> psim.similarity('ab ba c', 'ab ba d') # Lower similarity since 'a' is common
    .6
    >>> psim.similarity('db bd c', 'db bd a') # Higher similarity since 'd' is rare
    .8


Custom types

.. code:: python

    >>> from match.similarity import ProbabilisticDiceCoefficient
    >>> corpus = ''.join(['cheddar', 'brie', 'guyere', 'mozzarella', 'parmesian', 'jack', 'colby'])
    >>> cheese_sim = ProbabilisticDiceCoefficient(corpus)
    >>> match.add_type('cheese', StringType(similarity_measure=cheese_sim))
    >>> match.detect_type('colby jack')
    (.8, 'cheese')


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

