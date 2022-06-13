Built-in Doodads
=============================

.. contents:: Table of Contents
    :depth: 2

This section is meant to be about things built into the interpreter (or eventual compiler) directly.
There will eventually be a separate page for things corresponding to standard library modules.

Functions and Constants
-----------------------

Right now, the contents of Python's ``math`` module are exposed as global names, with a few exceptions.
Thus, for example, you could write ``4 * atan(1) - pi`` and the response should be ``0``.

Additionally, Python methods on Python objects are exposed within current Bedspread,
so that for example ``"Abracadabra".upper`` yields the string *ABRACADABRA*.
(Such support is necessarily slow and incomplete, since Python and Bedspread have different conventions.)

Pretty soon, I'll probably add some intrinsics for getting at tabular data,
because I'd like to put bedspread up to the task of orchestrating some statistical models
based on data from kaggle.com.
Operationally, the place to start would be csv files.

Named Operators
----------------

.. note:: This is planned. It does not yet work.

For arithmetic
...............
``mod``
    the modulus (i.e. remainder) operation. E.g. ``243 {mod} 7`` would evaluate to five.
``div``
    Truncated integer division. E.g. `243 {div} 17`` would be 14.

For collections
................
``at``
    Extract items from list, dictionary, or whatever else.
    The left argument is the list, while the right argument is either a scalar or list of keys/indices.
    Given a scalar right argument, you get a scalar result.
    Given a vector-type right argument, you get a vector result.
    Given a set-type right argument, you should probably get a dictionary, but that's up in the air.

Adverbs
---------

.. note:: This is planned. It does not yet work.

For now, these definitions are all in the context of single-level arrays.
They will have to grow as the language does.

``fold``
    Puts an infix operator between each element of a sequence *in sequence*, to produce a scalar result.
    In infix form, the arguments are effectively concatenated first according to their rank.

``pairwise``
    Puts an infix operator between each element of an array, to produce a new vector consisting of the results.
    In infix form, the arguments are effectively concatenated first according to their rank.

``reverse``
    Causes an infix operator to behave as though its arguments were reversed.



