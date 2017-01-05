==========================================
Searching for a declaration (using a loop)
==========================================

This example shows how to search for a specific declaration using a loop on the declarations tree.

Let's consider the following c++ file (example.hpp):

.. literalinclude:: example.hpp
   :language: c++
   :lines: 5-

The following code will show you how to loop on the tree and find a declaration

.. literalinclude:: example.py
   :language: python
   :lines: 6,7,8,17-27,29-
