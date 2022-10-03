Journal: The History and Future of System Development
======================================================

.. contents:: Table of Contents
    :depth: 2

June 2022
-----------
The first thing out was a proof-of-concept for a grammar that had been knocking around between my ears.
A parser generated syntax nodes with methods for a polymorphism-based recursive-descent pretty-printer.
Then I built a simple strict evaluator that ran on syntax nodes directly.
However, since the evaluator is itself written in a high-level language (Python)
The evaluation context was just a ``collections.ChainMap`` representing static scope.

July 2022
-----------
I added an analogue to static nested scopes and some simple product-types
through a simplistic integration with SQLite.
The concept was that each definition would have its own database record with different fields for
parameters, expression body, name, comments, and whatever else. Subordinate definitions would be
linked into a tree structure. One field distinguished different types of expression: either
normal code, a constant text, or a template meant for string interpolation.
This worked in some respects and was a fun experiment, but was hard to edit, navigate, etc.

August 2022
------------
Pretty much nothing happened to this code.
I was focused on the upstream module that handles the grammar and parsing.

September 2022
---------------
Slow month, but I refreshed my understanding of call-by-need (Thank you SICP) and an abstract VM concept.
The result went into a self-contained set of "toy" code and tests which you can find outside the main module.
The toy code does not integrate with a parser, but just evaluates its own structures.

October 2022
-------------
I now anticipate a progression of incremental improvements over the simple call-by-need core.
But first, I will require some initial domain of application.
Games and Turtle Graphics would both be a good starts.
Maybe I make a logo-like toy language to give some nice visual appeal to the activity.

