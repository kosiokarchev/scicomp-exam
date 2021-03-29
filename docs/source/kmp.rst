Problem 1: KMP
==============

The Knuth–Morris–Pratt [KMP]_ algorithm for locating a needle in a haystack (if,
of course, the needle and haystack are ordered sequences and the needle is not
infinite). This is not a particularly difficult task if you are smart enough to
fugure out a "(non-)backtracking table" which helps you exploit the fact that
you already *know* the "characters" you looked at.

`kmp_search`\ [#]_ works as you would expect (or not?):

>>> kmp_search('Waldo', 'Where\'s Waldo?')
8
>>> kmp_search('', '')
0
>>> kmp_search('love', 'a hopeless place')  # None

It is faster, due to a better algorithmic complexity, than the naïve
search-at-every-position approach\ [#]_ and scales asymptotically the same as
the builtin subsequence search routines in Python. There is a mere
:math:`\sim 426 \times` difference in the constant; however, we totally don't care
about it.

.. image:: _static/kmp.*
    :align: center

.. rubric:: Footnotes

.. [#] It is a rather perverted one-liner: see `the source of kmp_search
    <_modules/scicomp/exam/kk/kmp.html#kmp_search>`_. In fact, the table
    initialisation can be further inlined, but enough is enough.

.. [#] Also a one-liner: ``first((i for i in range(len(haystack) - len(needle))
    if haystack[i:i+len(needle)] == needle), None)`` using `more_itertools.first`.

----------

.. automodule:: scicomp.exam.kk.kmp
    :members:

----------

.. rubric:: References

.. [KMP] Knuth, Donald; Morris, James H.; Pratt, Vaughan (1977). "Fast pattern
    matching in strings". SIAM Journal on Computing. **6** (2): 323–350.
    doi:`10.1137/0206024 <https://doi.org/10.1137%2F0206024>`_.
