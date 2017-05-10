==========================
Elaborated type specifiers
==========================

Elaborated type specifiers are one of these four possibilities: *class*, *struct*, *union* or *enum*.

In C++ they can often be skipped (but may be useful; see `this interesting topic`_ for example).
In C code they are mandatory.

Let's consider the following c++ file:

.. literalinclude:: example.hpp
   :language: c++
   :lines: 5-

The following code will show how the elaborated type specifiers are treated in pygccxml.
Please note that this feature is only available since recent versions of *CastXML* (Mar 1, 2017),
and a special flag needs to be passed to pygccxml to make this work (castxml_epic_version=1).

.. literalinclude:: example.py
   :language: python
   :lines: 6,7,8,17-27,29-

.. _`this interesting topic`: http://stackoverflow.com/questions/1675351/typedef-struct-vs-struct-definitions/1675446#1675446