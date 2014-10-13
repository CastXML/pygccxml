pygccxml
========

.. image:: https://travis-ci.org/gccxml/pygccxml.svg?branch=master
    :target: https://travis-ci.org/gccxml/pygccxml
.. image:: https://coveralls.io/repos/gccxml/pygccxml/badge.png?branch=master
    :target: https://coveralls.io/r/gccxml/pygccxml?branch=master

pygccxml is a specialized XML reader that reads the output from GCCXML. It provides a simple framework to navigate C++ declarations, using Python classes.

Install
-------

You can use pip to install pygccxml:

  pip install pygccxml

To install from source, you can use the usual procedure:

  python setup.py install

Contact us
----------

You can contact us through the gccxml mailing list: http://www.gccxml.org/mailman/listinfo/gccxml

For issues with pygccxml you can open an issue here: https://github.com/gccxml/pygccxml/issues

Documentation
-------------

For examples and tutorials see the documentation: http://pygccxml.readthedocs.org

Branches
--------

The stable version can be found on the master branch.

The develop branch containes the latest improvements but can be unstable. Pull Requests should be done on the develop branch.

Testing and code coverage
-------------------------

pygccxml has more than 200 unit tests. They are run after each code commit to ensure
that the code stays functional and stable. You can find the builds here:
https://travis-ci.org/gccxml/pygccxml/builds

Code coverage is also available. It is automatically updated after each commit and can be found here:
https://coveralls.io/r/gccxml/pygccxml
