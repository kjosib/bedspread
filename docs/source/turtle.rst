Turtle Graphics
===================

.. note::
	This section is hypothetical, for the time being.

Turtle-graphics are a fun way to play and learn programming.
The original used a call-by-value procedural language
and thus imposed a strict sequencing discipline for procedure.
Moving the turtle counts as procedural activity and so temporal sequence is a critical component.

Bedspread aims for call-by-need, but for the time being we can establish a nice binding between the two paradigms.
A bedspread function that evaluates to a sequence of turtle-control instructions can
control a turtle no less powerfully than the original procedural paradigm,
but can also take advantage of call-by-need along the way.

Postulate a primitive function (i.e. written in Python, for now) which accepts a *lazy* list of turtle instructions.
That function can call upon BedSpread's internal lazy-evaluation machinery to extract instructions in sequence,
then carry them out in a sort of fetch-execute loop.

This sounds restrictive, but it's a start. Other things can come later.

This requires at minimum a concept of a lazy cons cell.
But for convenience's sake, I'd like to have a normal type-algebra.
So that means getting product and sum types working first.

