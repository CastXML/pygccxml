Building the documentation
==========================

Building the documentation locally
----------------------------------

You can build the documentation yourself. In order for this to work you need
sphinx doc (http://sphinx-doc.org) and the readthedocs theme:

    pip install sphinx

    pip install sphinx_rtd_theme

Then just run the following command in the root folder:

  make html

This will build the documentation locally in the `docs/_build/html` folder.

For each commit on the master and develop branches, the documentation is
automatically built and can be found here: https://readthedocs.org/projects/pygccxml/
