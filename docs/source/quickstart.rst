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

    Bed Spread (version 0.0.0), interactive REPL
        Documentation is at http://bedspread.readthedocs.io
        This is pre-alpha code. Current goal is to pretty-print ASTs corresponding to expressions.
        ctrl-d or ctrl-z to quit, depending on operating system
    Ready >>

In this mode, **Bed Spread** functions much like a powerful scientific calculator:
you can type in a mathematical expression and get an answer back.::

    Ready >> 7 + 12
    19
    Ready >>

Nice, eh? Except... What does it even mean?

    Things will get quite a bit better still as more features come along.

Or if **Bed Spread** didn't quite understand what you meant,
it will point out where it got confused trying to read what you wrote.

**Bed Spread** expressions work much like the formulas in a typical spreadsheet program.
The main differences are:

* There are no cells to reference, and thus no cell references.
* There is syntax for making choices among alternatives.
* You can create and alter your own functions easily. (Coming soon!)
* You can access the full capabilities of your computer. (Eventually.)
* Comparatively little actually works just yet.


**For the technically minded:**
*Bed Spread* aims to be a relatively pure functional language with lazy evaluation.
At this very moment, evaluation is strict, but that will change in time.
