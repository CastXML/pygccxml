Releasing
=========

Preparation
-----------

Run `git checkout develop`.

To build a new release, modify the version number in:

``pygccxml/__init__.py``

This version number will then automatically be used to build
the documentation and by the setup.py script when building the wheels.

Run `git add . && git commit -m "Bump version major.minor.minor"`.

Do not forget to document the latest changes in the ``CHANGELOG.md`` file.

Merging and releasing
---------------------

Merge develop into master:

Run `git merge develop master`.

Tag the version (do not forget the v):

Run `git tag vmajor.minor.minor`.

Run `git push origin v2.0.0 && git push origin master`

Wait for the CI checks to run before uploading the release to pypi.

Uploading to pypi
-----------------

The documentation for the building and uploading can be found here: `pypi`_

Cleanup your dist:

``rm -rf dist``

The wheels are built with:

``python3 setup.py bdist_wheel --universal``

They are uploaded with:

``twine upload dist/*``


.. _`pypi`: http://python-packaging-user-guide.readthedocs.org/en/latest/distributing/
