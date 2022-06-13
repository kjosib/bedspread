.. Bed Spread documentation master file, created by
   sphinx-quickstart on Sun May 15 04:35:18 2022.

Bed Spread: an Expression-Oriented Code-in-Database System
==========================================================

*Bed Spread* aims to re-imagine and reshape the act of programming in a high-level computer language
as a richly semantic interaction with a deeply structured and assistive database of functionality.
Also, it's still pre-alpha. A text-console-hosted evaluator works, with four kinds of definitions in a database.
Next goal is a graphical shell by July.

.. note:: **Bed Spread** is still being invented. Things *will* change, but I'll try to keep the documentation up to date.

.. toctree::
   :maxdepth: 2

   about
   quickstart
   grammar
   data
   intrinsic
   derived
   simpleIO
   fileIO
   turtle
   games
   share
   dbi
   ffi
   hacking

You can also visit the `github page <https://github.com/kjosib/bedspread>`_ if you'd like to follow development.

For the technically minded:
   *Bed Spread* aims to be a relatively pure functional language with both lazy evaluation
   and strong vector-oriented powers resembling those of APL,
   but legible to the causal user.
   There's a tension between these aspects. It will be interesting to see how that resolves.
   At this very moment, evaluation is strict/eager, but that will change in due time.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
