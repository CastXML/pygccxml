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
html files in the documentation folder. Then it will automatically commit the
changes. You will then have time to review the changes and push them to
origin/gh-pages.

This script was setup and adapted from here:
http://blog.nikhilism.com/2012/08/automatic-github-pages-generation-from.html

Moving to a new version of sphinx
---------------------------------

If you update the docs with "make gh-pages", and the sphinx version you use
is different than the previously used one, this will result in many changes
in the files due to the version change. To prevent this, a version check
was added in the sphinx Makefile in the root directory.

When you are ready for a sphinx update, you need to update the needed version
number in the Makefile and commit this change.
