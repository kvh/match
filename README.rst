===============================
Match - Probabilistic Entity Detection and Matching in Python
===============================


.. image:: https://img.shields.io/pypi/v/match.svg
        :target: https://pypi.python.org/pypi/pymatch

.. image:: https://img.shields.io/travis/kvh/match.svg
        :target: https://travis-ci.org/kvh/match

.. image:: https://readthedocs.org/projects/match/badge/?version=latest
        :target: https://match.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/kvh/match/shield.svg
     :target: https://pyup.io/repos/github/kvh/match/
     :alt: Updates


* Free software: MIT license
* Documentation: https://match.readthedocs.io.

Match brings common-sense entity detection and matching to python. Match is:

* Dead-simple to use
* Fast
* Lightweight (no heavy dependencies)
* Magic!

Installation
--------

* TODO

Usage
--------

Auto-detect common entity types

.. code:: python

    >>> import match


    >>> match.detect_type('608-555-5555')
    (1, 'phonenumber')

    >>> match.detect_type('joe.van.gogh@example.com')
    (1, 'email')

    >>> match.detect_type('John R. Smith')
    (.95, 'fullname')

    >>> match.detect_type('Hi, how are you?')
    (1, 'string')

    >>> match.score_types('@squaredloss: match v0.2.0 is out!')
    [(0, 'email'), (.05, 'fullname'), (0, 'phonenumber'), (1, 'string'), (0, 'datetime'), ...


Intelligently score similarity based on detected type

.. code:: python

    >>> match.score_similarity('Jonathan R. Smith', 'john r smith')
    (.82, 'fullname') # Similar, but common name

    >>> match.score_similarity('Jayden R. Smith', 'jayden r smith')
    (.93, 'fullname') # Similar, but uncommon name, so higher match probability

    >>> match.score_similarity('123 easy st, NY, NY', '123 Easy Street, New York City')
    (.98, 'address')

    >>> match.score_similarity('223 easy st, NY, NY', '123 easy st, NY, NY')
    (.6, 'address') # Locations are close but unlikely to be the same physical place (barring a typo)

    >>> match.score_similarity('Hi, how are you Joe?', 'hi how are you doing joe?')
    (.81, 'string')

    >>> match.score_similarity('608-555-5555', '608-555-5554', as_type='phonenumber')
    .0

    >>> match.score_similarity('608-555-5555', '608-555-5554', as_type='string')
    .9


Parse normalized entity representations

.. code:: python

    # As string
    >>> match.parse('(608) 555-5555')
    ('+1 608 555 5555', 'phonenumber')

    >>> match.parse('6085555555')
    ('+1 608 555 5555', 'phonenumber')

    # As object
    >>> match.parse(' march 3rd, 1997', to_object=True)
    (datetime.datetime(1997, 3, 3), 'datetime')

    >>> match.parse_as(' march 3rd, 1997', 'email')
    None


Probabilistic similarities, based on frequencies in a given corpus.

.. code:: python

    >>> from match import similarities
    >>> import random


    # Build similarity model from weighted random corpus of a's, b's, c's, and d's
    >>> corpus = [''.join(random.sample('a'*10000 + ' '*10000 + 'b'*1000 + 'c'*100 + 'd'*10, k=10)) for _ in range(1000)]
    >>> model = match.build_similarity_model(corpus, model_type='tfidf', tokenizer='2grams')
    >>> model.similarity('ab ba c', 'ab ba d')
    .6  # Lower similarity since 'a' is common

    >>> model.similarity('db bd c', 'db bd a')
    .8  # Higher similarity since 'd' is rare

    # Use in high-level api
    >>> match.score_similarity('db bd c', 'db bd a', similarity_measure=model)
    .8


    # Efficient similarity lookups with indexing (requires numpy and pandas, optional requirements)
    >>> model.build_index() # Requires O(n*k) space, where n is number of docs and k is average doc length
    >>> len(model.get_all_similar('db bd c', measure='overlap', threshold=.6))
    48 # O(k) similarity search


Custom type detection and scoring

.. code:: python

    >>> from match.similarity import ProbabilisticDiceCoefficient


    # Build similarity model from custom corpus
    >>> corpus = ['cheddar', 'brie', 'guyere', 'mozzarella', 'parmesian', 'jack', 'colby']
    >>> model = match.build_similarity_model(corpus, model_type='dice', tokenizer='3grams')
    >>> match.add_type('cheese', similarity_model=model)
    >>> match.detect_type('colby jack')
    (.8, 'cheese')


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

