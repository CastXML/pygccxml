pygccxml
========

The purpose of `pygccxml` is to read a generated xml file and provide a simple
framework to navigate C++ declarations, using Python classes.

Using `pygccxml` you can:

* Parse C++ source code
* Create a powerful code generator
* Generate UML diagrams
* Build code analyzers
* ...

Installation
============

Installation instructions can be found here: :doc:`Installation <install>`

Examples
========

The :doc:`examples <examples>` are a good way to learn how to use `pygccxml`.

`pygccxml` provides a powerful API. If you want to know more about the provided API
read the :doc:`query interface <query_interface>` document or the
:doc:`API documentation <apidocs/modules>`.

Contributing
============


License
=======

`Boost Software License`_.

Test environment
================

`pygccxml` comes with comprehensive unit tests. They are executed on different operating systems,
and with different versions of compilers. See the `Travis`_ builds for more details.
`pygccxml` is tested under python 2.6, 2.7, 3.2, 3.3, 3.4, 3.5. All in all, `pygccxml` has more than 230 tests.


Documentation contents
======================

.. toctree::
   :maxdepth: 1

   install
   examples
   faq
   apidocs/modules
   documentation
   query_interface
   design
   users
   links
   releasing
   history
   upgrade_issues

.. _`Boost Software License`: http://boost.org/more/license_info.html
.. _`Travis`: https://travis-ci.org/gccxml/pygccxml/builds
.. _`boost::type_traits` : http://www.boost.org/libs/type_traits/index.html


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
