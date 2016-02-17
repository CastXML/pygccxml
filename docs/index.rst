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

Installing
==========

You can use pip to install pygccxml::

  pip install pygccxml

To install from source, you can use the usual procedure::

  python setup.py install

Examples
========

The :doc:`examples <examples>` are a good way to learn how to use `pygccxml`.

`pygccxml` provides a powerful API. If you want to know more about the provided API
read the :doc:`query interface <query_interface>` document or the
:doc:`API documentation <apidocs/api>`.

Contributing
============


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
   examples
   documentation
   query_interface
   design
   upgrade_issues
   users
   links
   releasing
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
