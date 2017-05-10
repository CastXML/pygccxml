==============
Compound types
==============

A type is a compound_t type (in pygccxml) if it is one of the following:
*volatile_t*, *restrict_t*, *const_t*, *pointer_t*, *reference_t*,
*elaborated_t*, *array_t* or *member_variable_type_t*.

The exact c++ definition of compound types embraces more types, but for different
reasons (mostly legacy), the definition in pygccxml is slightly different.

Let's consider the following c++ file:

.. literalinclude:: example.hpp
   :language: c++
   :lines: 5-

The following code will show what to expect from compound types, how they are
chained, and how their order is defined in pygccxml.

.. literalinclude:: example.py
   :language: python
   :lines: 6,7,8,17-27,29-
