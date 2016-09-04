==========================================
Searching for a declaration (using a loop)
==========================================

This example shows how to search for a specific declaration using a loop on the declarations tree.

Let's consider the following c++ file (example.hpp):

.. literalinclude:: example.hpp
   :language: c++
   :lines: 4-

The following code will show you how to loop on the tree and find a declaration

.. literalinclude:: example.py
   :language: python
   :lines: 5,6,7,16-26,28-
