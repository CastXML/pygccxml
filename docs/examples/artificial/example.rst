========================================
Explicit and implicit class declarations
========================================

Even if a class has no explicit constructor, ``pygccxml`` will provide
a constructor declaration. This is due to ``CastXML`` and ``GCC-XML`` generating
implicit constructors (for example copy constructors) in their XML output.
The same thing holds for assignment operators and destructors.

To be able to discriminate between the different types of declarations,
the ``decl.is_artificial`` attribute can be used.

Let’s consider the following c++ file (example.hpp):

.. literalinclude:: example.hpp
   :language: c++
   :lines: 5-

In this example, the constructor is explicitly defined. The declaration tree
will contain two constructors. The first one is the one we defined explicitly,
and is not marked as artificial. The second one is the copy constructor, which was
implicitly added, and is marked as artificial.

.. literalinclude:: example.py
   :language: python
   :lines: 6,7,8,17-27,29-
