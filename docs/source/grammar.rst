The *Bed Spread* Expression Grammar
========================================

.. contents:: Table of Contents
    :depth: 2

Literals
----------

Currently, the only base data type is the number.
You can write them in scientific notation if you like: ``6.02e+23`` is Avogadro's number, for example.
You can also use hexadecimal: ``$ffff`` is 65,535 in decimal.
(You can also use ``0x`` or ``#`` to prefix a hex numeral.)
And you can split digit groups with the underscore character: ``1_000_000_000`` is more clearly
equal to ``1e9`` than is ``1000000000``.

Eventually there will be more interesting data types.

Names
---------

The naming convention for variables in *Bed Spread* is similar to most modern programming languages:
start with a letter, then are allowed letters, digits, and underscores.
There are no identifiers starting with underscore at this time because that's a terrible hack that we should not need.

At the moment, names are case sensitive, but I'll probably change that in a future version.

Keywords
----------
Some names (like ``and``) are off-limits as identifiers because they are keywords with special meaning in the language.
All keywords are independent of case. (For instance, you could spell it ``AND`` or even ``aNd``.)
However, names may absolutely contain components that might otherwise look like keywords.
Thus, both ``sand`` and ``andrew`` are valid identifiers.

Arithmetic
----------

Arithmetic looks like you learned in school: ``+``, ``+``, ``*``, ``/`` for the basic four functions.
Exponentiation is ``^`` and right-associative, so ``3^3^3`` is equal to ``3^27``, which is a very big number.

Parentheses work like you would expect for grouping. That is, ``3 + 4 * 5`` is 23, but ``(3 + 4) * 5`` is 35.
For clarity, you may also use square brackets like ``[ 123 + 456 ]`` for grouping.
The round and square brackets must nest and balance properly.

The keyword ``MOD`` stands for the modulus (i.e. remainder) operation. It has the same precedence and associativity
as multiplication and division.

Relational Operators
----------------------

You can compare quantities using ``<`` ``<=`` ``=`` ``!=`` ``>=`` ``>``.
In a nod to other languages, you can use ``==`` as a synonym for ``=``,
and you can use ``<>`` as a synonym for ``!=`` (i.e. *does-not-equal*).
The result of any such comparison is a Boolean True/False quantity.
Relational comparisons have lower precedence than arithmetic.

Function Calls
--------------

Function application also looks like you're used to from math class.
For instance, the cosine of the square of ``x`` could be written as ``cos(x^2)``.
The (round) parentheses are necessary in this case to indicate that you're applying a function.

Functions with more than one parameter take keyword-arguments (only).
For example, there's a built-in function ``atan2`` which takes an X-Y coordinate and
gives you back the corresponding angle, taking the sign of both arguments into account.
You can call it as ``atan2(x:1, y:2)`` or ``atan2(y:1, x:-2)``.

An interesting thing you can do with functions of more than one parameter is
called "partial application": By supplying *just some* of the arguments,
this creates a new function in which only the other parameters remain.
So, in the above example, you could write ``atan2(x:1)(y:2)`` and it would do the right thing.

Logical Operators
---------------------

* ``AND``, ``OR``, and ``NOT`` work in the usual way.
* ``EQV`` means *logical equivalence:* either both true or both false.
* ``XOR`` means *exclusive-or:* either, but not both, are true.

They're also not case-sensitive, so you can use lower-case if you prefer (and I do so prefer).
``NOT`` binds more tightly than the other logical operators,
but there is otherwise no precedence relationship between them:
they work strictly from left to right.

Selection among Alternatives
----------------------------

You can write an expression like ``{ when a > b then c; when d < e then f; else g }``
and it will mean either ``c``, ``f``, or ``g`` according to the values of the other variables.
Once again, the keywords ``WHEN``, ``THEN``, and ``ELSE`` are not case-sensitive.

The curly braces specifically mean an alternative selection form is enclosed.
They are inspired by mathematical notation for a function defined in parts.

Lambda Forms
-------------

Don't let the Greek letter scare you. This is just how you pass functionality around.
Once the system around the language is a bit more developed, these may be less tempting
because it will always be possible to give some fragment of function a name.

An expression like ``\ x [ x + x ]`` means "a function that returns double its argument.
You can pass it as a parameter to another function, or you can call it directly
just as if it were the name of a function. (In fact, on the inside, function names
simply refer to objects like this.)

A form like the above, with a single parameter, takes a single anonymous argument.
If you need more than one parameter, simply separate them with commas.
For an extended example::

    \a,b,c[ (b + sqrt(b^2 - 4*a*c)) / (2*a) ] (a:2, b:4, c:-8)

is how you might write, and then immediately use, a function that returns one root of a quadratic equation.

Inside the square brackets, you can use any name known outside them,
plus also the new names introduced as parameters.

Because there is no ambiguity, you can use round parentheses if you prefer.
You can also go with curly braces for a parameterized selection.

Let / Where / Recursive Definitions
-------------------------------------

The plan is that user-defined and *named* functions will go into a database,
along with information about what's considered to be in scope where.
All named functions will allow recursive calls.

Also, the long-term plan is lazy evaluation and tail-recursion elimination.
Those features are not yet in place:
they'll require some significant adjustments to the evaluator.

