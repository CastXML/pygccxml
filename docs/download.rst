==================
Download & Install
==================

-------------------------
pygccxml on SourceForge
-------------------------

pygccxml project is hosted on SourceForge. Using SourceForge services you
can:

1) get access to source code
2) get access to latest release version of pygccxml


-----------------
Subversion access
-----------------

http://sourceforge.net/svn/?group_id=118209

--------
Download
--------

https://sourceforge.net/project/showfiles.php?group_id=118209

------------
Installation
------------

GCC-XML
-------
There are few different ways to install GCC-XML on your system:

1. If you use Linux, than I am almost sure your system has "gccxml" package.
   Consider to install it using "native"(rpm, deb, portage) packaging system.

.. line separator

2. Another option is to install it from the source code. See `instructions`_
   provided by Brad King, the author of `GCC-XML`_. Installation from sources
   is supported for Windows, Linux and Mac platforms.

.. _`instructions` : http://gccxml.org/HTML/Install.html

pygccxml
--------
In command prompt or shell change current directory to be "pygccxml-X.Y.Z".
"X.Y.Z" is version of pygccxml. Type the following command:

| ``python setup.py install``

After this command complete, you should have installed pygccxml package.

------------
Dependencies
------------

* `GCC-XML`_

.. _`GCC-XML`: http://www.gccxml.org
