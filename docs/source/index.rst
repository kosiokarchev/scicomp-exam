Scientific Computing and Algorithms @ SISSA 2021
================================================

*Exam solutions by Kosio Karchev*


.. toctree::
    kmp.rst
    bwt.rst
    lzw.rst


.. Indices and tables
   ==================
    * :ref:`genindex`
    * :ref:`modindex`
    * :ref:`search`

----------

.. rubric:: General note
Motivated by the fact that this library is a one-off effort intended as a
demonstration of coding and algorithmic thinking abilities, and that it
contains exclusively atomic implementations of well-defined (finalised)
algorithms, the style of the code it contains is guided less by the usual
factors---readability, maintainability, and others defined in the `Zen of Python
<https://www.python.org/dev/peps/pep-0020/>`_---and much more by the intent of
"having fun with coding" and (ab)using the "cool features" of the language, as
subjectively determined by the author, resulting in numerous superfluous
iterator comprehensions, variable definitions therein\ [#]_, and various other
one-liner "hacks".

.. [#] Note that as of Python 3.9 (`bpo-32856 <https://bugs.python.org/issue32856>`_)
    definitions like ``(... for name in [value])`` are accelerated internally
    and equivalent in performance to usual name binding like ``name = value``.
