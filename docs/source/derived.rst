Make your own Functions
==========================

In *bedspread,* the functions you create are kept in a database.
A specialized editor is *meant to become* part of the package.

.. note:
    For the moment, that database is a file called ``functions.bedspread``.
    In the first phase, it will be this ugly thing where you need a separate database editor.
    But that will be the motivation to produce a simple graphical program editor,
    and then it's all downhill from there. Probably.

User Interface Concept
----------------------

In concept, the goal is that the user-interface should provide a nice structured view of:

* Name
* Parameters
* Prose Description
* Scenarios, each consisting of:
    * an expression bound to each parameter.
    * a predicate-expression indicating whether the computed answer is as anticipated.
    * the actual computed result -- perhaps color coded pass/fail/error
* The formula that defines the function. This might be a:
    * single text area for a normal function.
    * structured grid for a function defined by parts.
* A sensible variety of ways to navigate amongst definitions.
* A sensible organizational structure for definitions.

You might reasonably want several such windows open at once.

So anyway, that's the future.


The Topic System
-----------------

The concept here is that a particular consistent set of parameters might be relevant to several functions.
These might reasonably form a *topic* in a sense similar to that of linguistics.

.. note:: The topic system is still under construction. There will probably be subtopics.
