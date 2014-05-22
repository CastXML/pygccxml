Building the documentation
==========================

Building the documentation locally
----------------------------------

You can build the documentation yourself. In order for this to work you need
sphinx doc (http://sphinx-doc.org). Then just run the following command
in the root folder:

  make html

This will build the documentation locally in the docs/_build/html folder.

Updating the documentation on github
------------------------------------

This is for the pygccxml maintainers. You need to have push access to the
github repository to do this.

The documentation is hosted on github through the github pages service.
You can find it at http://gccxml.github.io/pygccxml/

To update the documentation, run the following command in the root folder.

  make gh-pages

You can find more details in the Makefile about this command. It will
checkout to the gh-pages branch, build the documentation, update the
html files in the documentation folder. Then it will commit the changes
and push it automatically to origin/gh-pages.

This script was setup and adapted from here:
http://blog.nikhilism.com/2012/08/automatic-github-pages-generation-from.html
