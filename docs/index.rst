pygccxml
========

The purpose of `pygccxml` is to read a generated file and provide a simple
framework to navigate C++ declarations, using Python classes.

What can you do with it?
------------------------
Using `pygccxml` you can:

* parse C++ source code
* create a powerful code generator

  + `Py++ <http://sourceforge.net/projects/pygccxml/files/pyplusplus/>`_ is heavily based on `pygccxml`
  + generate `WSDL`_ file from sources
  + ...

* generate UML diagrams
* build code analyzer
* ...

Query interface
---------------
`pygccxml` provides simple and powerful API to query declarations tree.

How many lines are needed to write the following query?
::

  select all free functions from the project
  where
      name equal to "do_smth"
      return type is void
      function has two arguments
      second argument type is int

Only single line of code is needed:

.. code-block:: python

  # global_ns is the reference to declarations, which describes the global(::) namespace
  # "None" means any type.
  global_ns.free_functions("do_smth", return_type="void", arg_types=[None, "int"])

If you want to know more about provided API read the :doc:`query interface <query_interface>`
document or the :doc:`API documentation <apidocs/api>`

Type traits
-----------
`pygccxml` provides a lot of functionality to analyze C++ types and relationship
between them. For more information please refer to the :doc:`design <design>` document or
the :doc:`API documentation <apidocs/api>`. A few examples:

* ``is_convertible(from, to)``

  returns ``True`` if there is a conversion from type ``from`` to type ``to``,
  otherwise ``False``

* ``is_unary_operator(oper)``

  returns ``True`` if ``oper`` describes an unary operator


Declaration dependencies
------------------------
You can query a declaration, about it dependencies - declarations it depends on.
This is a very powerful and useful feature. `Py++ <http://sourceforge.net/projects/pygccxml/files/pyplusplus/>`_, for example, uses this functionality to check that user creates Python
bindings for all relevant declarations.

Caching
-------
Consider the following situation: you have to parse the same set of files every
day. There are 2 possible ways to complete the task:

* create a header file that includes all files you need to parse

* parse each file separately and then join the results

The difference between these approaches is the caching algorithm used in the
second case. `pygccxml` supports both of them. Actually `pygccxml` supports
more caching strategies, read the API documentation for more information.

Binary files parser
-------------------
`pygccxml` contains a functionality which allows to extract different information
from binary files (`.map`, `.dll`, `.so`) and integrate it with the existing
declarations tree.

License
=======

`Boost Software License`_.

Test environment
================

`pygccxml` comes with comprehensive unit tests. They are executed on the `Ubuntu`_ Linux operating systems.
See the `Travis`_ builds for more details. `pygccxml` is tested under python 2.6, 2.7, 3.2, 3.3 and 3.4.
All in all, `pygccxml` has more than 230 tests.


Documentation contents
======================

.. toctree::
   :maxdepth: 1

   download
   documentation
   query_interface
   design
   upgrade_issues
   example/example
   users
   links
   history
   credits
   apidocs/api

.. _`WSDL`: http://www.w3.org/TR/wsdl
.. _`SourceForge`: http://sourceforge.net/index.php
.. _`Docutils`: http://docutils.sourceforge.net
.. _`Python`: http://www.python.org
.. _`GCC-XML`: http://www.gccxml.org
.. _`Boost Software License`: http://boost.org/more/license_info.html
.. _`Ubuntu`: http://www.ubuntu.com/
.. _`Travis`: https://travis-ci.org/gccxml/pygccxml/builds
.. _`boost::type_traits` : http://www.boost.org/libs/type_traits/index.html


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

