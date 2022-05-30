Foreign Function Interface
=============================

At the moment, the ``evaluator`` module has a global dictionary called ``GLOBAL_SCOPE``.
You can add values here by name before invoking ``evaluator.evaluate(tree)``.
If you want them callable, you should make either an ``evaluator.PythonUnary`` or an ``evaluator.PythonMultary``.

Presently, ``PythonMultary`` attempts to pass all parameters positionally. It should be possible for
an interested person to take better advantage of introspection to handle keyword-only parameters.
Finally, Python's flexible-to-a-fault signature system means some functions won't translate as-is
to **Bed Spread**'s slightly more rigid worldview of *zero, one, or keywords*. For example,
``math.hypot`` is defined in terms of ``*args`` which is not a thing in **Bed Spread**.

By the way, the ``evaluator`` module also how has a function called ``FFI`` which does most of the work
to create a correct entry suitable for insertion into the ``GLOBAL_SCOPE``.
Also, field access uses this on callable fields, so in some cases you might could just insert the module itself.

.. note::
    Eventually, the scope rules may change so that submodules need to mention what they depend on.

