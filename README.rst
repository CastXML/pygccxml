pygccxml
========

.. image:: https://travis-ci.org/gccxml/pygccxml.svg?branch=develop
    :target: https://travis-ci.org/gccxml/pygccxml
    :alt: Unit tests status
.. image:: https://coveralls.io/repos/gccxml/pygccxml/badge.svg?branch=develop
    :target: https://coveralls.io/r/gccxml/pygccxml?branch=develop
    :alt: Code coverage status
.. image:: https://readthedocs.org/projects/pygccxml/badge/?version=develop
    :target: https://readthedocs.org/projects/pygccxml/?badge=develop
    :alt: Documentation status
.. image:: https://www.quantifiedcode.com/api/v1/project/117af14ef32a455fb7b3762e21083fb3/snapshot/origin:develop:HEAD/badge.svg
    :target: https://www.quantifiedcode.com/app/project/117af14ef32a455fb7b3762e21083fb3?branch=origin%2Fdevelop&tab=basics
    :alt: Code quality status

pygccxml is a specialized XML reader that reads the output from CastXML or GCCXML. It provides a simple framework to navigate C++ declarations, using Python classes.

Install
-------

You can use pip to install pygccxml:

  pip install pygccxml

To install from source, you can use the usual procedure:

  python setup.py install

Contact us
----------

You can contact us through the CastXML mailing list: http://public.kitware.com/mailman/listinfo/castxml

For issues with pygccxml you can open an issue here: https://github.com/gccxml/pygccxml/issues

Documentation
-------------

For examples and tutorials see the documentation: http://pygccxml.readthedocs.org

Branches
--------

The stable version can be found on the master branch.

The develop branch contains the latest improvements but can be unstable. Pull Requests should be done on the develop branch.

Testing and code coverage
-------------------------

pygccxml has more than 200 unit tests. They are run after each code commit to ensure
that the code stays functional and stable. You can find the builds here:
https://travis-ci.org/gccxml/pygccxml/builds

Code coverage is also available. It is automatically updated after each commit and can be found here:
https://coveralls.io/r/gccxml/pygccxml
