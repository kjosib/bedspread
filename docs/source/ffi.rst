Foreign Function Interface
=============================

At the moment, the ``evaluator`` module has a global dictionary called ``GLOBAL_SCOPE``.
You can add values here by name before invoking ``evaluator.evaluate(tree)``.
If you want them callable, you should make either an ``evaluator.PythonUnary`` or an ``evaluator.PythonMultary``.

