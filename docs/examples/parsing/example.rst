==================
Parsing a c++ file
==================

This example shows how to setup pygccxml to parse a c++ file, and how
to access the declaration tree.

Let's consider the following c++ file (example.hpp):

.. literalinclude:: example.hpp
   :language: c++
   :lines: 5-

The following code will show you how to create a configuration for
the xml generator (an external tool, either castxml or gccxml),
and how to parse the c++ file:

.. literalinclude:: example.py
   :language: python
   :lines: 6,7,8,17-27,29-
