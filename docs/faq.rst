FAQ
===


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
