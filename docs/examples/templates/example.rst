=============
C++ Templates
=============

pygccxml has minimal support for c++ templates, but there is some information
that can be extracted from templated declarations.

Let's consider the following c++ file (example.hpp):

.. literalinclude:: example.hpp
   :language: c++
   :lines: 5-

This example show how to extract template parameters from the template declaration.

.. literalinclude:: example.py
   :language: python
   :lines: 6,7,8,17-27,29-
