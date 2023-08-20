Releasing
=========

Preparation
-----------

Run `git checkout develop`.

To build a new release, modify the version number in `pyproject.toml`.

This version number will then automatically be used to build
the documentation and by the build script when building the wheels.

Run `git add . && git commit -m "Bump version major.minor.minor"`.

Do not forget to document the latest changes in the ``CHANGELOG.md`` file.

Merging and releasing
---------------------

Merge develop into master:

Run `git checkout master`.

Run `git merge develop master`.

Tag the version (do not forget the v):

Run `git tag vmajor.minor.minor`.

Run `git push origin vmajor.minor.minor && git push origin master`

Wait for the CI to be done and all green.

Go to the releases page on github and use the "draft a new release" button
to create a new release. Use the exisiting tag. You can copy-past the
changelog's content there if you want to.

Once you are done, you can upload the release to pypi.

Uploading to pypi
-----------------

The documentation for the building and uploading can be found here: `pypi`_

Cleanup your dist:

``rm -rf dist``

Make sur your build tools are up to date

`python3 -m pip install --upgrade build`

The wheels and the source distribution are built with:

``python3 -m build``

They are uploaded with:

``twine upload dist/*``


.. _`pypi`: http://python-packaging-user-guide.readthedocs.org/en/latest/distributing/
