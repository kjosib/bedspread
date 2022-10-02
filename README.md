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

* [x] Decide on host language for initial development (Python)
* Langauge Characteristics
  * [x] Typical math-like functional expression grammar with a right-associative selection form.
  * Text/string support
    * [x] Grammar for simple constant strings
    * [x] Long-strings and templates (done as `symbol`-table entries)
    * [ ] Proper text-oriented operators and functions
    * [ ] Regular-expression support
  * [ ] Streaming/collection/list facility
  * [x] Product-types (i.e. records) and field access expressions
  * [ ] Sum-types (i.e. unions) and type-case matching for functions
  * [ ] Lazy Evaluation
  * [ ] Something akin to block-scope nesting 
  * [ ] Type Safety
  * [ ] Do something about external effects. This may involve monads or a cool process-algebra.
* Programmer-Interface Features
  * [x] Console-hosted read-parse-display loop
  * [x] Console-hosted read-eval-print loop (REPL) without stored functions, but with intrinsics and lambda forms.
  * [ ] Error context must be tied to the function source at issue.
  * [ ] Make the REPL poll for a changed database before evaluating immediate-mode expressions.
  * [ ] Minimal graphical shell: a console, a function index with search facility, and a clause editor.
  * [ ] More advanced facilities -- to be determined
* Code-in-Database Features:
  * [x] Minimal database schema for UDFs, and a few simple samples.
  * [x] Adjust REPL to pull UDFs from a database.
    * [ ] Fix error reporting in UDFs to blame the guilty function, which is more about the evaluator.
  * [ ] Abstract over DB access to isolate the concern.
  * [ ] Add schema and REPL support for access to foreign function interface.
* Interface to the environment (needs support for a process model of some kind)
  * [ ] Simple console I/O
  * [ ] File I/O
    * [ ] Universal Streaming Concept
    * [ ] Sequential Binary and Text (with codecs)
    * [ ] Random access
    * [ ] Record-structuring
  * [ ] Sophisticated console I/O
    * [ ] ncurses-style colors and cursor control
    * [ ] keyboard/mouse/timer event loop
  * [ ] Turtle Graphics (Perhaps there's a turtle monad?)
  * [ ] Raster Graphics, which might live within...
  * [ ] Windowing / GUI Tooling, which could be tkinter on Python or JavaFX on JVM.
  * [ ] Arcade-Game Facilities
    * [ ] Sprites / Textures
    * [ ] 3-D Graphics
    * [ ] Full-Screen Mode
    * [ ] Music and Sound Effects


## Documentation:

Documentation is [at readthedocs](https://bedspread.readthedocs.io/en/latest/).

## Application to Education

The specific STEM skill exposure to this system should most improve is functional abstraction. 

Part of the plan is to get turtle graphics into the mix fairly early on.
Also, the aim is an approachable, highly interactive, and supportive functional programming system.
Once students have a grasp of mathematical syntax, they should be able to write formulas for fun and profit.
The on-screen supportive development environment should remove most frustrations associated with large code files.
Once *Bed Spread* is in shape for it, I would welcome the help of educators to build curricula based on
subsets of the complete system and aligned either with concurrently-taught topics,
or perhaps something kids enjoy like making and playing games (e.g. 2-D side scrollers like "Flighty Avian").

