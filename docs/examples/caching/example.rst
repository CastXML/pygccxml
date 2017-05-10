=======
Caching
=======

This example shows how to use caching. This can be useful
for big projects where you don't want the c++ to be parsed
again and again.

Let's consider the following c++ file:

.. literalinclude:: example.hpp
   :language: c++
   :lines: 5-

To enable caching, you can use the following code:

.. literalinclude:: example.py
   :language: python
   :lines: 6,7,8,17-27,29-

The first time you run this example, the c++ file will be read and a xml
file will be generated:

INFO Creating xml file "example.hpp.xml" from source file "example.hpp" ...
INFO Parsing xml file "example.hpp.xml" ...
My name is: ns

The second time you run the example the xml file will not be regenerated:

INFO Parsing xml file "example.hpp.xml" ...
My name is: ns

Of course the performance gain will be small for this example,
but can be intersting for bigger projects.
