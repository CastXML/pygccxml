Download & Install
==================

Prerequisite: CastXML
---------------------

`CastXML`_ needs to be installed on your system.

1) If you are on linux or mac, your package manager may already provide a "castxml" package.

2) You can download pre-compiled binaries for `Linux`_, for `OS X`_ and for `Windows`_.

3) You can compile CastXML from source, either with the `SuperBuild`_, or by following the `full install instructions`_ .


Installation of pygccxml
------------------------

You can use pip to install pygccxml:

.. code-block:: shell

    pip install pygccxml

To install from source, you can use the usual procedure:

.. code-block:: shell

  python setup.py install

For development
%%%%%%%%%%%%%%%

You should use a ``virtualenv`` when possible. Example recipe:

.. code-block:: shell

  cd pygccxml  # git root
  python -m virtualenv ./venv
  source ./venv/bin/activate
  pip install --editable .[test]

GCC-XML (Legacy)
----------------

These instructions are only here for historical reasons. `GCC-XML`_ was the tool used
to generate the xml files before CastXML existed.

**From version v1.8.0 on, pygccxml uses CastXML by default.
The support for GCC-XML will finally be dropped in pygccxml v2.0.0.**

There are few different ways to install GCC-XML on your system:

1) Most Linux system provide the "gccxml" package through their package manager.

2) See the `instructions`_ to install GCC-XML from source.

.. _`instructions`: http://gccxml.org/HTML/Install.html
.. _`GCC-XML`: http://www.gccxml.org
.. _`CastXML`: https://github.com/CastXML/CastXML
.. _`Linux`: https://midas3.kitware.com/midas/folder/13152
.. _`OS X`: https://midas3.kitware.com/midas/folder/13152
.. _`Windows`: https://midas3.kitware.com/midas/folder/13152
.. _`SuperBuild`: https://github.com/thewtex/CastXMLSuperbuild
.. _`full install instructions`: https://github.com/CastXML/CastXML#build
