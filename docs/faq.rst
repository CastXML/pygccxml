FAQ
===

GCCXML vs CastXML
-----------------

``GCCXML`` has been superseded by ``CastXML``. It is highly recommended to
use ``CastXML``. ``GCCXML`` support will be removed from ``Pygccxml``
in version 2.0.

C++ and C code support
----------------------

``Pygccxml`` supports ``C++98``, as ``CastXML`` and ``GCCXML`` only output
declarations from the ``C++98`` subset. Of course, newer versions of C++
can be parsed (the tests currently all pass with ``C++11`` and ``C++14``),
but not all new features from these language definitions can be used.

``C`` code support has been reported to work. As ``C`` is similar to ``C++``,
this makes sense. Some discrepancies may be present.

Still, parsing ``C`` code is not officially supported by ``pygccxml``, as it
falls out of scope of this project. Of course, if some volunteer wants to work
on this, submissions would be accepted.

Function and method bodies
--------------------------

``Pygccxml`` does not allow to fetch declarations defined in function or method
bodies. For example the following ``a`` variable will not appear in
the declarations tree:

 | int f() {
 |   int a = 3;
 |   return a;
 | }

Neither ``GCCXML`` or ``CastXML`` currently support this feature.
``CastXML`` could probably be extended for this later, as ``pygccxml``.

Performance
-----------

pygccxml is being regularly optimised for performance, but it still may be slow
in certain cases.

Before all, it is highly recommended to benchmark your application if performance
is important to you. There are multiple tools out there for benchmarking python
applications. We currently are using the following two command lines / tools:

 | python -m cProfile -o profile_data.pyprof script_to_profile.py
 | pyprof2calltree -i profile_data.pyprof -k

Of course optimising pygccxml alone will not help in all cases. The bottlenecks can also be
in the code calling pygccxml, to make sure to benchmark the whole process.
Any help on the performance side is also welcome.

Some things you may try (in order of priority):

1) You might want to consider making the declaration tree as small as possible
   and only store those declarations that somehow have an influence on the bindings.
   Ideally, this is done as early as possible and luckily castxml and gccxml
   provide an option that allows you to reduce the number of declarations that
   need to be parsed.

   You can specify one or more declarations using the ``-fxml-start`` (gccxml) or
   ``-castxml-start`` (castxml) options when running the xml generator. For
   example, if you specify the name of a particular class, only this class
   and all its members will get written. Ideally, your project should already use
   a dedicated namespace, which you can then use as a starting point.
   All declarations stemming from system headers will be ignored (except
   for those declarations that are actually used within your library).

   In the pygccxml package you can set the value for these flags by using
   the ``start_with_declarations`` attribute of the ``pygccxml.parser.config_t``
   object that you are passing to the parser.

2) You can pass the following flag to the *read_files* method:

      compilation_mode=pygccxml.parser.COMPILATION_MODE.ALL_AT_ONCE

3) If you want to cache the declarations tree, there is a caching mechanism provided
   by pygccxml. You will find an example of this mechanism in the examples section.


Flags
-----

castxml_epic_version
--------------------

The ```castxml_epic_version``` can be set to 1 to benefit from new castxml
and pygccxml features. To be able to use this, you will need the latest
castxml version.

Currently this adds the support for elaborated type specifiers.

\_\_va_list_tag and other hidden declarations (f1)
--------------------------------------------------

When parsing with CastXML, the XML tree can contain declarations named
``__va_list_tag``. If the compiler is llvm 3.9,  ``__NSConstantString_tag``
and ``__NSConstantString`` declarations may also be present.

These declarations are internal declarations, coming from the std c++ library
headers you include, and are often not needed. They are for example polluting
the declarations tree when running pyplusplus.

By default, pygccxml will ignore these declarations.
To still read these declarations from the xml file, a config flag can
be set (``config.flags = ["f1"]``), or a flag can be passed as argument the
config setup (``flags=["f1"]``).

\_\_thiscall\_\_ in attributes (f2)
-----------------------------------

Attributes defined as ```__thiscall__``` are now ignored (tested with VS 2013).
The ```__thiscall__``` in some attributes will be removed too. If you still
want to have access to these attributes, you can use the
``config.flags = ["f2"]`` option.
