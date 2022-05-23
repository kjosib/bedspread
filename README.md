# Bed Spread: an Expression-Oriented Code-in-Database System

In late 1979, Visicalc plugged a domain-specific pure-functional programming language into a
rectangular grid on a personal computer, and lo, how the world was changed.
But outside of spreadsheets and a few smug exceptions,
virtually all other programming today is *still* done as (collections of)
long text files.

This project represents an attempt to do for general-purpose programming
what Visicalc did for run-of-the-mill data modelling, presentation, and analysis.

Let us build a small functional programming system that does not rely for block-structuring
on anything that behaves too much like conventional text files.
Let each declaration be a record (or several) in a relational database.
And let there be a simple proof-of-concept UI for navigating, reading, editing, and running code.

This has many interesting consequences. Some examples:

* Extract documentation with but a simple SQL query.
* No more crazy quoting: Long strings, complex regular expressions, even comments just go in separate records tagged with their kind.
* Parsing is vastly simplified for the same reason: wacky quoting machinery need not be considered, specified, or implemented.
* Custom extra attributes on code objects are as simple as adding fields in a database. Oh, and tweaking the reference UI to respect them.
* Existing generic database editors make usable interim tooling for bootstrapping an ecosystem.

Results are in progress, and conclusions are to be determined.
There's a paper under construction, and when finished it will most likely be put someplace public.

## Development Roadmap

Note: *UDF* here stands for *User-Defined Function*.

* [x] Decide on host language for initial development (presumably Python)
* [x] Hack together a typical math-like functional expression grammar with a right-associative selection form.
* [x] Console-hosted read-parse-display loop
* [x] Console-hosted read-eval-print loop (REPL) without stored functions, but with intrinsics and lambda forms.
* [ ] Minimal database schema for UDFs, and a few simple samples.
* [ ] Adjust REPL to pull UDFs from a database.
* [ ] Abstract over DB access to isolate the concern.
* [ ] Add Lazy Evaluation.
* [ ] Add Strings.
* [ ] Add Turtle Graphics. This may be cause to do something about monads, or at least add a semicolon.
* [ ] Minimal graphical shell: a console, a function index with search facility, and a clause editor.
* [ ] Add algebraic types, first to the schema, then the grammar, then
* [ ] Do something about monads. This may involve
* [ ] Add schema and REPL support for access to foreign function interface.


## Documentation:

Documentation is [at readthedocs](https://bedspread.readthedocs.io/en/latest/).
A first-draft list of headings is:

* Starting with *Bed Spread*: How to open the REPL and play
* The *Bed Spread* expression grammar
* Functions you can use, right out of the box
* Make your own functions
* Simple Input and Output
* Data Structures
* I/O with Files:
  * Structured
  * Free-form
* Turtle Graphics
* Games
* Sharing your project
* Bindings to components written in other languages
* System Internals

## Application to Education

The specific STEM skill exposure to this system should most improve is functional abstraction. 

Part of the plan is to get turtle graphics into the mix fairly early on.
Also, the aim is an approachable, highly interactive, and supportive functional programming system.
Once students have a grasp of mathematical syntax, they should be able to write formulas for fun and profit.
The on-screen supportive development environment should remove most frustrations associated with large code files.
Once *Bed Spread* is in shape for it, I would welcome the help of educators to build curricula based on
subsets of the complete system and aligned either with concurrently-taught topics,
or perhaps something kids enjoy like making and playing games (e.g. 2-D side scrollers like "Flighty Avian").

