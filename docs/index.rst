pygccxml
========

pygccxml is a specialized XML reader that reads the output from CastXML.
It provides a simple framework to navigate C++ declarations, using Python classes.

Using pygccxml you can:

* Parse C++ source code
* Create a code generator
* Generate UML diagrams
* Build code analyzers
* ...

Installation
------------

Installation instructions can be found here: :doc:`Installation <install>`

Compatibility
-------------

pygccxml is compatible with Python 2.7, 3.4, 3.5, pypy and pypy3.

Documentation and examples
--------------------------

The :doc:`examples <examples>` are a good way to learn how to use pygccxml.

If you want to know more about the API provided by pygccxml, read the :doc:`query interface <query_interface>` document or the :doc:`API documentation <apidocs/modules>`.

A `FAQ <faq>`_ is also available and may answer some of your questions.

License
-------

`Boost Software License <http://boost.org/more/license_info.html>`__

Contact us
----------

You can contact us through the `CastXML mailing list <http://public.kitware.com/mailman/listinfo/castxml/>`__.

For issues with pygccxml you can open an issue `here <https://github.com/gccxml/pygccxml/issues/>`__.

Branches
--------

The stable version can be found on the master branch.

The develop branch contains the latest improvements but can be unstable. Pull Requests should be done on the develop branch.

Test environment
----------------

You can find the Mac and Linux builds `here <https://travis-ci.org/gccxml/pygccxml/builds>`__.
The Windows builds are located `here <https://ci.appveyor.com/project/iMichka/pygccxml>`__.

Running the test suite is done with:

.. code-block:: python

  python3 -m unittests.test_all

Code coverage is also available. It is automatically updated after each commit and can be found `here <https://coveralls.io/r/gccxml/pygccxml>`__.

Documentation contents
----------------------

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

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
