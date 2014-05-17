pygccxml
========

pygccxml is a specialized XML reader that reads the output from GCCXML. It provides a simple framework to navigate C++ declarations, using Python classes.

Install
-------

The package uses the Python distutils so you can do the usual procedure:

  python setup.py install

For more information about using the distutils see the Python manual
"Installing Python Modules".

Documentation
-------------

For examples and tutorials see the pygccxml web site.

You can build the documentation yourself. In order for this to work you need
sphinx doc (http://sphinx-doc.org). This can be done using the following
command in the docs folder:

  make html

Testing
-------

pygccxml has more than 200 unit tests. They are run after each code commit to ensure
that the code stays functional and stable. You can find the builds here:
https://travis-ci.org/gccxml/pygccxml/builds
