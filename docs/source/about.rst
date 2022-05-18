Introduction: About Bed Spread
=================================

The Vision
---------------
*Bed Spread* aims to re-imagine and reshape the act of programming in a high-level computer language
as a richly semantic interaction with a deeply structured and assistive database of functionality.
This represents an attempt to do for general-purpose computer-programming
what the spreadsheet did for most common forms of data modelling and
analysis -- but with a completely new and different set of mistakes.


Historical Context
---------------------------------
In 1979, Visicalc (the first spreadsheet program) changed the world. Its interactive nature, consistent model,
comfortable learning curve, and natural applicability represent a conceptual leap
that computing may never see again. The grid-based interface and library of built-in
mathematical, statistical, and financial functions transformed microcomputers thenceforth into
something virtually anyone could actually use for real work.
Spreadsheets have been *the answer* for run-of-the-mill data modelling and analysis ever since.
Oh by the way, spreadsheets are also a grid-structured functional programming language:
completely pure, but possessed of `a host of shortcomings <https://en.wikipedia.org/wiki/Spreadsheet#Shortcomings>`_
and `prone to weird behavior <https://en.wikipedia.org/wiki/Microsoft_Excel#Conversion_problems>`_

In stark contrast, virtually all other nontrivial programming has stuck with the way of giant text
documents stuffed stem to stern with code and, with luck, some commentary also.
It has been this way ever since the punched card's demise at the hands of timesharing systems connected to teletypes.
This begat an entire galaxy of tools, systems, and techniques specifically for dealing acceptably with code files
and the organizational busywork they create.


Current Status
---------------
*Bed Spread* is presently too nascent for serious use, but watch this space.

.. _roadmap:

Development Roadmap
--------------------

Note: *UDF* here stands for *User-Defined Function*.

* [x] Decide on host language for initial development (presumably Python)
* [x] Hack together a typical math-like functional expression grammar with a right-associative selection form.
* [x] Console-hosted read-parse-display loop
* [ ] Console-hosted read-eval-print loop (REPL) without UDFs, but with intrinsics for the basics.
* [ ] Minimal database schema for UDFs, and a few simple samples.
* [ ] Adjust REPL to pull UDFs from a database. (Abstract over DB access to isolate the concern.)
* [ ] Add Lazy Evaluation.
* [ ] Add Turtle Graphics. This may be cause to do something about monads, or at least add a semicolon.
* [ ] Minimal graphical shell: a console, a function index with search facility, and a clause editor.
* [ ] Add algebraic types, first to the schema, then the grammar, then
* [ ] Do something about monads. This may involve
* [ ] Add schema and REPL support for access to foreign function interface.

