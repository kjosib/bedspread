Getting Started: How to open the REPL and play
===============================================

Install (or Upgrade)
--------------------

To install **Bed Spread**, you must first have `Python. <https://www.python.org/>`_
Then, at a console prompt, type::

    pip install --upgrade bedspread

Expect a bunch of progress messages.
If you have trouble,
someone familiar with installing Python packages may be able to help you out.

First Run
----------

At that same console, type::

    py -m bedspread

Right now, the very first version of *Bed Spread* is still under construction.
That's why it currently uses a text-only console interface.
Eventually, the plan is to do something graphical and pretty.
Meanwhile, there's a vague resemblance to the 1980s.

You'll see something like:

.. code-block:: text
    :caption: Don't expect much quite yet. This is still pre-alpha.

    quadratic : One root of a quadratic expression.
    cons : The standard elementary unit of list linkage.
    greet : Sample template.
    Bed Spread (version 0.0.1), interactive REPL
        Documentation is at http://bedspread.readthedocs.io
        This is pre-alpha code. Current goal is to pretty-print ASTs corresponding to expressions.
        ctrl-d or ctrl-z to quit, depending on operating system
    Ready >>

In this mode, **Bed Spread** functions much like a powerful scientific calculator:
you can type in a mathematical expression and get an answer back.::

    Ready >> 7 + 12
    19

You can also invoke functions in the usual way, by giving their argument in parenthesis::

    Ready >> sin(pi/2)
    1.0
    Ready >> sin(pi/3)^2
    0.7499999999999999
    Ready >> greet("Ian")
    Hello, Ian! Nice to meet you.
    Ready >> quadratic(a:1, b:2, c:-16)
    3.1231056256176606
    Ready >>

Nice, eh? Except... What does it all mean?

Or if **Bed Spread** didn't quite understand what you meant,
it will point out where it got confused trying to read what you wrote.::

    Ready >> "alpha" beta
    At line 1, column 9:
     >>> "alpha" beta
                 ^^^^-- near here
    <<Error: (8, 4) Syntax Error>>
    Ready >>

**Bed Spread** expressions work much like the formulas in a typical spreadsheet program.
Full details are given in :doc:`grammar`. The key conceptual differences are:

* There are no cells to reference, and thus no cell references.
* There is syntax for making choices among alternatives, dealing with structured data, and all the rest.
* You can create and alter your own functions easily.
* **Bed Spread** aims to (eventually) provide access to the full capabilities of your computer.

About Creating Functions
-------------------------

Have a look in your current working directory. (On Windows, type ``start .``.)
If you look carefully, you'll see a file called ``functions.bedspread``.
This is in fact a very small SQLite database.

.. note::
    Eventually, there's to be a nicer user-interface to manage all this,
    so you don't need a separate SQLite table editor.
    Remember, this is all still in a very early stage.

Open it with your favorite SQLite manager and have a look at the contents of the table called "symbol".
You can add your own formulas using a language described in a later section of this manual.
Also, this is how you'd define custom data types and text blocks.

