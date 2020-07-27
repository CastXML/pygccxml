Releasing
=========

To build a new release, modify the version number in:

``pygccxml/__init__.py``

This version number will then automatically be used to build
the documentation and by the setup.py script when building the wheels.

Do not forget to document the changes in the ``CHANGELOG.md`` file.

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
