pygccxml
========

.. image:: https://travis-ci.org/gccxml/pygccxml.svg?branch=develop
    :target: https://travis-ci.org/gccxml/pygccxml
    :alt: Linux and Mac tests status
.. image:: https://ci.appveyor.com/api/projects/status/knt8ej6vp1w76may/branch/develop?svg=true
    :target: https://ci.appveyor.com/project/iMichka/pygccxml
    :alt: Windows tests status
.. image:: https://coveralls.io/repos/gccxml/pygccxml/badge.svg?branch=develop
    :target: https://coveralls.io/r/gccxml/pygccxml?branch=develop
    :alt: Code coverage status
.. image:: https://readthedocs.org/projects/pygccxml/badge/?version=develop
    :target: http://pygccxml.readthedocs.io/en/develop/?badge=develop
    :alt: Documentation status

pygccxml is a specialized XML reader that reads the output from CastXML or GCCXML. It provides a simple framework to navigate C++ declarations, using Python classes.

Install
-------

Install instructions can be found `here <http://pygccxml.readthedocs.io/en/master/install.html>`_.

Documentation and examples
--------------------------

The documentation can be found `here <http://pygccxml.readthedocs.io>`_, examples can be found `here <http://pygccxml.readthedocs.io/en/master/examples.html>`_.

A `FAQ <http://pygccxml.readthedocs.io/en/master/faq.html>`_ is also available and may answer some of your questions.

Contact us
----------

You can contact us through the `CastXML mailing list <http://public.kitware.com/mailman/listinfo/castxml/>`_.

For issues with pygccxml you can open an issue `here <https://github.com/gccxml/pygccxml/issues/>`_.

Branches
--------

The stable version can be found on the master branch.

The develop branch contains the latest improvements but can be unstable. Pull Requests should be done on the develop branch.

Testing and code coverage
-------------------------

pygccxml has more than 250 unit tests. They are run after each code commit to ensure
that the code stays functional and stable. You can find the Mac and Linux builds `here <https://travis-ci.org/gccxml/pygccxml/builds>`_ and
the Windows builds `here <https://ci.appveyor.com/project/iMichka/pygccxml>`_.

Running the test suite is done with:

.. code-block::

  python3 -m unittests.test_all

Code coverage is also available. It is automatically updated after each commit and can be found `here <https://coveralls.io/r/gccxml/pygccxml>`_.
