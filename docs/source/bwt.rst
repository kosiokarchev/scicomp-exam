Problem 2: BWT
==============

`Wikipedia <https://en.wikipedia.org/wiki/Burrows%E2%80%93Wheeler_transform#Sample_implementation>`_
has a sample Python implementation of the Burrows-Wheeler transform. Let's
one it up and write a one-liner:\ ::

    map(last, sorted(circular_shifts(s + '\0')))

Arguably, we need `more_itertools.circular_shifts` (`source <https://more-itertools.readthedocs.io/en/stable/_modules/more_itertools/more.html#circular_shifts>`_)
and `more_itertools.last` (`source <https://more-itertools.readthedocs.io/en/stable/_modules/more_itertools/more.html#last>`_),
but they are also essentially one-liners with error-prone padding and some
preparation.

This is naïve and "slow". The alternative implementation here follows
[F11]_, itself after [OS09]_, and as per the assignment uses suffix arrays. As
a result it has linear time complexity.\ [#]_ [#]_ Turns out that even with all
the bloat and Python involved, it is faster than the naïve variant for
sequences above around 1000 elements. In addition, the memory requirements are
"reasonable" (i.e. again linear) in contrast to the naïve method that requires
storing all cyclic permutations at the same time for the sorting.

.. image:: _static/bwt-runtime.*
    :align: center

Finally, the claim in the problem statement is that BW encodings are more
compressible. We verify this for random strings (and our own implementation of
LZW compression!):

.. image:: _static/bwt-compression.*
    :align: center

Looks like I should have said "refute this": for random strings there is no
difference between compressing the original and the BWT: supposedly, they are
both equally random; structured (and entertaining) text\ [#]_, however, suffers
noticeably from being weirdly transformed: the structures captured by the LZW
algorithm are destroyed by the BW transform.\ [#]_

.. rubric:: A note on the implementation

In contrast to the codes in the other "modules" in this library, the
implementation of the BWT does not focus (so much) on one-liner-ness. As such,
it contains functions and even classes! The main workhorse is `SABucket` that,
naturally, represents a "character bucket" for the suffix array construction.
A hierarchy of helper classes is present in `bwt.collections
<scicomp.exam.kk.bwt.collections>`, while the suffix array-related
functionality resides in `bwt.suffix_array <scicomp.exam.kk.bwt.suffix_array>`.
Some thoughts and comments can be found throughout the source code, but they
will not be expanded upon in the documentation.

.. rubric:: Footnotes

.. [#] The only caveat is the complexity in terms of the alphabet size, which
    is definitely not linear in our implementation since it requires sorting
    "character" buckets. Nevertheless, we are working under the paradigm that
    the given sequences are much longer than the alphabet size.

.. [#] To do the inverse transformation also in linear time, we follow a recipe
    by [G11]_, which relies on being extremely clever.

.. [#] It is left as an exercise to the reader to guess the "corpus" used. A
    hint can be found at the end of the discussion of `Problem 3: LZW`.

.. [#] For reference, the compression level reaches 65% for the "meaningful"
    text. There is a slight tendency towards decreasing of the "BWT surplus"
    for very long sequences, which we do not explore.

----------

.. py:currentmodule:: scicomp.exam.kk.bwt
.. autofunction:: bwt_encode
.. autofunction:: bwt_decode

----------

.. rubric:: References

.. [F11] Fischer, Johannes (2011). *Inducing the LCP-Array*. Algorithms
    and Data Structures. Lecture Notes in Computer Science. **6844**. p. 374.
    arXiv:`1101.3448 <https://arxiv.org/abs/1101.3448>`_.
    doi:`10.1007/978-3-642-22300-6_32 <https://doi.org/10.1007%2F978-3-642-22300-6_32>`_.

.. [OS09] D. Okanohara and K. Sadakane. A linear-time Burrows-Wheeler
    transform using induced sorting. *Proc. SPIRE*. **5721**. pp. 90–101.
    Springer, 2009.

.. [G11] Gusfield, Daniel (2011). A linear time BWT inversion method.
    `<https://www.cs.ucdavis.edu/~gusfield/cs224f11/BWTcs224.pdf>`_
