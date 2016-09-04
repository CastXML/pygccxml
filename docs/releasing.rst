Releasing
=========

To build a new release, the following files should be modified:

Modify the version numbers in:

``setup.py`` (version and download_url)

``pygccxml/__init__.py``

``docs/conf.py``

Do not forget to document the changes in the ``CHANGELOG.md`` file.

Uploading to pypi
-----------------

The documentation for the building and uploading can be found here: `pypi`_

The wheels are built with:

``python setup.py bdist_wheel --universal``

They are uploaded with:

``twine upload dist/*``


.. _`pypi`: http://python-packaging-user-guide.readthedocs.org/en/latest/distributing/
