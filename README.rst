pygccxml
========

.. image:: https://readthedocs.org/projects/pygccxml/badge/?version=develop
    :target: http://pygccxml.readthedocs.io/en/develop/?badge=develop
    :alt: Documentation status

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

Install instructions can be found `here <http://pygccxml.readthedocs.io/en/master/install.html>`__.

Compatibility
-------------

pygccxml is compatible with Python 3.9, 3.10, 3.11, 3.12, 3.13 and pypy3.

Documentation and examples
--------------------------

The documentation can be found `here <http://pygccxml.readthedocs.io>`__, examples can be found `here <http://pygccxml.readthedocs.io/en/master/examples.html>`__.
You can also run an example JupyterLab Notebook using Binder, or view it using
``nbviewer``:

..
    Developers: See `.binder/README.md` for more information.

.. image:: https://mybinder.org/badge_logo.svg
    :target: https://mybinder.org/v2/gh/EricCousineau-TRI/pygccxml/feature-py-notebook-example?urlpath=tree/pygccxml/docs/examples/notebook/
    :alt: Binder
.. image:: https://img.shields.io/badge/view%20on-nbviewer-brightgreen.svg
    :target: https://nbviewer.jupyter.org/github/EricCousineau-TRI/pygccxml/tree/feature-py-notebook-example/docs/examples/notebook/
    :alt: nbviewer

If you want to know more about the API provided by pygccxml, read the `query interface <http://pygccxml.readthedocs.io/en/develop/query_interface.html>`__ document or the `API documentation <http://pygccxml.readthedocs.io/en/develop/apidocs/modules.html>`__.



A `FAQ <http://pygccxml.readthedocs.io/en/master/faq.html>`__ is also available and may answer some of your questions.

License
-------

`Boost Software License <http://boost.org/more/license_info.html>`__

Contact us
----------

For issues with pygccxml you can open an issue `here <https://github.com/CastXML/pygccxml/issues/>`__.

For issues with CastXML you can open an issue `here <https://github.com/CastXML/CastXML>`__.

You can contact us through the `CastXML mailing list <http://public.kitware.com/mailman/listinfo/castxml/>`__.

Branches
--------

The stable version can be found on the master branch.

The develop branch contains the latest improvements but can be unstable. Pull Requests should be done on the develop branch.

Testing
-------

Running the test suite is done with:

.. code-block::

  pytest tests
