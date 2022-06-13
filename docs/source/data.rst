Data Types
===========

This section is expected to grow soonish.

Numbers are currently all floating point. Strings are currently all unicode.

On the lambda-calculus side,
product-types are supported, but so far none are built in.
Meanwhile, sum-types are planned.
Data constructors have the syntax of function calls, so these share a namespace.

On the array/vector/matrix/collection side, so far it's just a plan.

One thing yet to be addressed is unbounded sequences.
Operationally, you can take any prefix but never consume the whole thing.

Incidentally, conflating *list-of-records* with *record-of-lists* might be worth some real consideration.
There is syntax for taking a field. Applied to an array of records, it could mean an array of fields.
This is basically what Pandas dataframes do. However, I have in mind to take this up a notch or two.
Also, I specifically *do not* mean to imply that Pandas will underlie everything.
(Anyway, that would be an irrelevant implementation detail.)

What about arrays of a sum type? In this case, the analogue to element access is type-case matching.

Probably the syntax ends up with an arrow glyph to indicate key/value pairs somehow.
And probably the common case of word-like keys looks a lot like what happens with function arguments now.
It's not clear how to denote empty dictionaries vs. empty lists, but maybe that can wait.

The one major design consideration for matrices / tensors is that dimensions will have names, not ordinal position.
So in other words, you don't get rows and columns. You get days of the week and product IDs.
Sure, an implementation might be forced to decide the low-level details, but they shouldn't be exposed without cause.

All of this means a bunch of things for a suitable evaluator.
Chiefly, values will need to grow tags.
The algebra of these tags (as distinct from the data that rides along) represents a design dimension.


