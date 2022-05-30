Make your own Functions
==========================
.. versionadded:: 0.0.1

In *bedspread,* the functions you create are kept in a database.
A specialized editor is *meant to become* part of the package.

.. contents:: Table of Contents
    :depth: 2


Defining Functions
-----------------------

You can define more functions by adding records to the ``symbol`` table in the database.
Use symbol kind ``formula`` for this. An example called ``quadratic`` starts in the database.

.. admonition:: About that crufty database

    The database is a SQLite file called ``functions.bedspread``.
    Eventually, there is to be a nice user-interface provided for this.
    Meanwhile, any random SQLite editor should serve in the interim.

The ``body`` field should contain an expression, same as what you might give to the interactive evaluator.
What's special is that you can use parameter names to stand in for whatever arguments are given at actual
calls to this function.

.. note::
    At the moment, all functions can see and call all other functions.
    Eventually there will be some concept of nested static scopes with visibility rules,
    but that would most likely be maddening without a purpose-built editor.

Text and Templates
-------------------
You can define a symbol in the database of kind ``text``,
in which case the ``body`` is treated as constant text to which you may refer by name.
An pre-loaded example is called ``Gettysbug``.

Alternatively, for a symbol of kind ``template``, the text in the ``body`` is considered a template:
placeholders are surrounded with curly braces. See the ``greet`` template for a simple example.
The names in the placeholders are used as the parameters, so it's not necessary to fill in the
``parameters`` field for a template. (In fact, it's ignored.)

.. note::
    Templates are currently implemented by giving the arguments to a template
    as keyword parameters to Python's ``str.format`` method. Thus, you get access
    to that formatting mini-language.

Defining Record Types
------------------------
In the database, you can define record-types by adding ``symbol`` records of kind ``record``.
The ``parameters`` field is taken to be a list of the fields of the record.


Future Plans
-------------------

*Precise details are subject to change.*

User Interface Concept
......................

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
......................
At some point, **Bed Spread** will probably need something serving a purpose similar to lexically-nested scope,
or as others call it, block-structuring.
In any event, that would mean some changes to the way evaluation gets done.
The author has in mind to try something a bit unconventional for the realm of pure-functional languages.
But details are still to be determined. Perhaps record-types get something like methods?

Record Validity Assertion
..........................
It might be interesting if the body of a ``record`` type-definition were to become a validity predicate.
There are probably some applications where this would be handy.
The downside is that it creates the potential for unstructured abort, although that can be managed in two ways:

* a *try-alternatives* expression, which may take several tries to get right
* a process algebra, which might be another avenue for extension
