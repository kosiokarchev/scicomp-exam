Problem 3: LZW
==============

Simple routines to encode/decode sequences using the Lempel–Ziv–Welch algorithm
[LZW]_. Note that this implementation does not deal with bytes and such. It
uses a bag of unbounded size (well, I guess `Py_ssize_t` although Python's
integer type claims to be unbounded, and so maybe are the sizes of collections)
and represents sequences of arbitrary elements as a sequence of integers. It is
the job of the user to provide an adequate initial "alphabet" to cover all
possible elements.

Wikipedia says "[t]he algorithm is simple to implement", and sure enough both
`lzw_encode` and `lzw_decode` are essentially one-liners with a bag
initialisation step to boot.

Here is an example:

>>> list(lzw_encode('supercalifragilisticexpialidocious', string.ascii_lowercase))
[18, 20, 15, 4, 17, 2, 0, 11, 8, 5, 17, 0, 6, 8, 33, 18, 19, 8, 2, 4, 23, 15, 8,
 32, 8, 3, 14, 2, 8, 14, 20, 18]

If you do the counting, you'll notice we saved two characters (compressed from
34 characters to 32 integers), accounting for the repetitions
supercalifragi-:underline:`li`-sticexpi-:underline:`al`-idocious (these get
indices 33 and 32 in the bag, respectively). You'll notice that LZW is a little
short-sighted since it only looks one character ahead (so that it can rebuild
the bag afterwards), and so it misses the opportunity to repeat the whole "ali"
the second time it occurs.

Round-tripping is exact only elementwise (i.e. strings get decoded as sequences
of characters). Also, decoding requires the alphabet again, which can be
annoying... or "useful" to e.g. make a needlessly complicated capitaliser:

>>> list(
...     lzw_decode(
...         lzw_encode('supercalifragilisticexpialidocious', string.ascii_lowercase),
...         string.ascii_uppercase))
['S', 'U', 'P', 'E', 'R', 'C', 'A', 'L', 'I', 'F', 'R', 'A', 'G', 'I', 'L', 'I', 'S',
 'T', 'I', 'C', 'E', 'X', 'P', 'I', 'A', 'L', 'I', 'D', 'O', 'C', 'I', 'O', 'U', 'S']


Since this is *scientific* computing, we will finish off with a plot. Have you
ever wondered how compressible the digits of :math:`\pi` in different bases are?\ [#]_

.. image:: _static/lzw-pi-bases.*
    :align: center

Implicit information is something I made up in order to have pronounced peak
and trough around 26 and 42. Get in touch if you want to know exactly what it
is.

.. [#] I know for one that :math:`\pi` in base-:math:`\pi` is very compressible!...

----------

.. py:currentmodule:: scicomp.exam.kk
.. autofunction:: lzw_encode
.. autofunction:: lzw_decode

----------

.. rubric:: References

.. [LZW] Welch, Terry (1984). "A Technique for High-Performance Data
    Compression". Computer. **17** (6): 8–19. doi:`10.1109/MC.1984.1659158
    <https://doi.org/10.1109%2FMC.1984.1659158>`_.
