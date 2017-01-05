================================
Parsing a string containing code
================================

This example shows how to setup pygccxml to parse a string containing c++ code,
and how to access the declaration tree. Often, pygccxml is used to parse files
containing code, but there may be reasons to parse a string (for example
for debugging purposes).

The following code will show you how to create a configuration for
the xml generator (an external tool, either castxml or gccxml),
and how to parse the string containing the c++ code:

.. literalinclude:: example.py
   :language: python
   :lines: 6,7,8,12-
