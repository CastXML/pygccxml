Building the documentation
==========================

Building the documentation locally
----------------------------------

You can build the documentation yourself. In order for this to work you need
sphinx doc (http://sphinx-doc.org) and the readthedocs theme:

.. code-block:: shell

  pip install .[docs]

Then just run the following command in the root folder:

.. code-block:: shell

  make html

This will build the documentation locally in the ``docs/_build/html`` folder.

For each commit on the master and develop branches, the documentation is
automatically built and can be found here: https://readthedocs.org/projects/pygccxml/
