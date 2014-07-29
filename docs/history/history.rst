Development history
===================

Introduction
------------

The original author and maintainer for pygccxml was Roman Yakovenko (2004-2011).
Holger Frydrych forked the project to work on python 3 support. Finally, Mark Moll
forked the project a second time to carry on the work of porting the code
to python 3 (keeping it compatible with python 2).
In Mai 2014, Michka Popoff and the Insight Software Consortium revived pygccxml
by setting up a git repositery on github, hosted along with gccxml.

About version numbers
---------------------

When the project moved to git, versions were tagged from 1.0.0 on. Note that
there was no 1.2, 1.3 nor 1.4 version (this is maybe due to the many forks
and the slow down of the maintenance effort).

Contributors
------------

Thanks to all the people that have contributed patches, bug reports and suggestions:

* Roman Yakovenko (original author)
* Roman Yakovenko's wife - Yulia
* Mark Moll
* Holger Frydrych
* John Pallister
* Matthias Baas
* Allen Bierbaum
* Georgiy Dernovoy
* Darren Garnier
* Gottfried Ganssauge
* Gaetan Lehmann
* Martin Preisler
* Miguel Lobo
* Jeremy Sanders
* Ben Schleimer
* Gustavo Carneiro
* Christopher Bruns
* Alejandro Dubrovsky
* Aron Xu

Version 1.6.2
-------------

1. Use setuptools instead of distutils for the packaging

2. Change rights of declarations_cache.py and templates_tester.py
   from -rwxr-xr-x+ to -rw-r--r--+, so that all the files have the same
   execution rights.

Version 1.6.1
-------------

1. Fix a regression introduced by previous changes. Syntax errors were introduced
   in the part were you can check if a class is copyable or not (see #13). These
   have been fixed now.

Version 1.6
-----------

1. Moved the repository from mercurial to git

2. Changed the documentation from epydoc to sphinx doc

3. Setup the documentation as gh-page and add script to update the documentation
   Just call "make gh-pages" on the root folder to create a commit with the
   new documentation, which you may then push to the github repository.
   The url for the documentation is now http://gccxml.github.io/pygccxml/

4. Add Travis unit tests for Python 2.6, 2.7, 3.2, 3.3 and 3.4
   The tests are run after each commit (see .travis.yml file in root folder)
   https://travis-ci.org/gccxml/pygccxml

5. Add automatic code coverage. The code coverage is run during each travis
   run and the results are uploaded to https://coveralls.io/r/gccxml/pygccxml

6. Fix copy_constructor unit test

7. Deprecate parser.config_t (replaced by parser.gccxml_configuration_t)

8. Fix for string comparison with future unicode literals
   When using from __future__ import unicode_literals in python 2.7,
   the call to the namespace() method would fail due to the isinstance/str
   check.

   A is_str() function was added to the utils module, allowing for a
   python 2 and python 3 compatible string check.
   A unit test for this case was added.

9. All the code is now pep8 compliant and is tested for this in an unit test

10. Most of unused imports and variables were removed using the pyflakes tool

11. Use new style python decorators (@property) everywhere

12. Add new unit test for the example.py file

13. Update the licence headers to reflect the change in maintainers

Version 1.5.2
-------------

1. Make python 3.x compatible. Still works with python 2.6 and python 2.7.

2. Add .dylib parser for Darwin

3. Fix some unit tests

4. workaround for problem with boost >=1.54

5. Simpler way of checksumming files in a python 2 and 3 compatible way

6. Prevent warnings to be treated as fatal errors in py++

7. "has_inline" property was added to ``declarations.calldef_t`` class.

8. Thanks to Aron Xu, for pointing out that it is better to use "os.name",
   instead of "sys.platform" for platform specific logic.

9. "__int128_t" and "__uint128_t" types were introduced. Many thanks to Gustavo Carneiro
    for providing the patch.

Version 1.5.1
-------------

1. adding problematic use case, contributed by Zbigniew Mandziejewicz

2. Adding "explicit" attribute to constructor_t class

3. "List symbols" (`nm`) utility invocation was improved and now handles
   right relative paths and paths with spaces. Many thanks to Alejandro Dubrovsky
   for providing the patch.

4. Fix for "get dependencies" functionality

5. Allow the process to continue, even in case the binary parser can not find the relevant declaration

6. Fix bug related to merging free functions

7. Improve decl_printer - sort declarations before printing

8. Added new tests and ported tests to x86_64 architecture

Version 1.5.0
-------------

1. Fix small bug in matcher - don't match namespaces by their location

2. Documentation update and cleanup. (using sphinx-doc now).

3. Fixing small bug on Windows, related to parsing configuration file

4. Update setup.py

5. fix 2779781 bug( pygccxml reverses array dimensions )

Version 1.1.0
-------------

1. bsc and mspdb packages were deprecated

2. Adding new functionality and improving initial environment handling

3. Adding ability to dump exported classes

4. Added more tests

5. Add handling for "C" functions

6. Fix bug "pygccxml parses const volatile variable args as just const"

7. Rename bparser to binary_parsers

8. Adding .so file parser

9. Replace md5 with hashlib module (removes deprecation warnings)

Version 1.0
-----------

1. Support for ellipsis was added.

   Warning: this feature introduce backward compatibility problem!

   Description:

   .. code-block:: c++

      void do_smth( int, ... )

   Before this change, pygccxml would report that the function ``do_smth`` has
   only one argument.

   After this change, pygccxml will report that the function has two arguments.
   The second argument type will be ``declarations.ellipsis_t``. All classes,
   which describe callables, have new property ``has_ellipsis``. It the value of
   the property is ``True``, than the function has ellipsis in its definition.

2. New experimental back-end, based on ``.pdb`` (progam database file), was added.

3. New high-level API wrapper for ``.bsc`` (browse source code file) was added.

4. The recomended GCC_XML version to use with this release is CVS revision 123.
   This revision introduces small, but very important feature. GCC_XML
   started to dump artificial declarations (constructor, destructor, operator=).
   ``pygccxml.declarations.type_traits`` functions were updated to use the new
   information.

5. ``declarations.decl_printer_t`` class dumps almost all available information
   about a declaration.

6. ``declarations.is_same_function`` was fixed and now it treats
   "covariant returns" right.

7. Search algorithm was improved for template instantiated classes. From
   now, a spaces within the class name doesn't matter.

8. pygccxml unit tests functionality was improved. Many thanks to Gustavo Carneiro.

Version 0.9.5
-------------

1. Class ``free_operator_t`` is now able to provide references to the class declarations
   instances it works on.

2. Support for `GCC-XML attributes`_ was added. Many thanks to Miguel Lobo for
   the implementation.

.. _`GCC-XML attributes`: http://www.gccxml.org/HTML/Running.html

3. A bug in parsing a function exception specification was fixed. Many thanks to
   Jeremy Sanders.

4. Support for a type/class "align", "offset" and "size" was added. Many thanks to
   Ben Schleimer for the implementation.

5. Support for GCC-XML 0.9 was added.

6. Support for ``__restrict__`` was added.

7. ``declarations.has_trivial_copy`` was renamed to ``declarations.has_copy_constructor``.
   The old name is still available, but will be removed soon.

8. ``declarations.priority_queue`` was renamed to ``declarations.priority_queue_traits``.

9. ``declarations.find_container_traits`` function was added.

10. Support for "partial name" was added. "Partial name" is the class name, without
    template default arguments. The functionality was added to std containers
    classes.

11. ``declarations.class_t`` and ``declarations.class_declaration_t`` has new property -
    ``container_traits``. This property describes std container element class.

12. All logging is now done to ``stderr`` instead of ``stdout``.

Version 0.9.0
-------------

1. Performance was improved. pygccxml is now 30-50% faster. The improvement
   was achieved by using `cElementTree`_ package, ``iterparse`` functionality,
   instead of standard XML SAX API. If `cElementTree`_ package is not available,
   the built-in XML SAX package is used.

.. _`cElementTree` : http://effbot.org/zone/celementtree.htm

2. ``is_base_and_derived`` function was changed. The second argument could be
   a tuple, which contains classes. The function returns ``True`` if at least one
   class derives from the base one.

.. line separator

3. Class ``calldef_t`` has property - ``does_throw``. It describes
   whether the function throws any exception or not.

.. line separator

4. Bug fixes: small bug was fixed in functionality that corrects GCC-XML reported
   function default arguments. Reference to "enum" declaration extracted properly.
   Many thanks to Martin Preisler for reporting the bug.

.. line separator

5. New type traits have been added:


   * ``is_std_ostream``
   * ``is_std_wostream``

.. line separator

6. C++ does not define implicit conversion between an integral type and ``void*``.
   ``declarations.is_convertible`` type traits was fixed.

.. line separator

7. ``declarations.is_noncopyable`` type traits implementation was slightly changed.
   Now it checks explicitly that class has:

   * default constructor
   * copy constructor
   * ``operator=``
   * destructor

   If all listed functions exist, than the algorithm returns ``False``, otherwise
   it will continue to execute previous logic.

.. line separator

8. ``declarations.class_declaration_t`` has new property - ``aliases``. This is
   a list of all aliases to the class declaration.

.. line separator

9. The message of the exception, which is raised from ``declarations.mdecl_wrapper_t``
   class was improved and now clearly explains what the problem is.

.. line separator

Version 0.8.5
-------------

1. Added new functionality: "I depend on them". Every declaration can report
   types and declarations it depends on.

2. ``signed char`` and ``char`` are two different types. This bug was fixed and
   now pygccxml treats them right. Many thanks to Gaetan Lehmann for reporting
   the bug.

3. Declarations, read from GCC-XML generated file, could be saved in cache.

4. New type traits have been added:

   * ``is_bool``

5. Small improvement to algorithm, which extracts ``value_type``
   ( ``mapped_type`` ) from "std" containers.

6. Few aliases to long method name were introduced:

   ================================= ==========================
                Name                           Alias
   ================================= ==========================
    ``scopedef_t.variable``           ``scopedef_t.var``
    ``scopedef_t.variables``          ``scopedef_t.vars``
    ``scopedef_t.member_function``    ``scopedef_t.mem_fun``
    ``scopedef_t.member_functions``   ``scopedef_t.mem_funs``
    ``scopedef_t.free_function``      ``scopedef_t.free_fun``
    ``scopedef_t.free_functions``     ``scopedef_t.free_funs``
   ================================= ==========================

7. Fixing bug related to array size and cache.

Version 0.8.2
-------------

1. Few small bug fix and unit tests have been introduced on 64 Bit platforms.
   Many thanks to Gottfried Ganssauge! He also help me to discover and fix
   some important bug in ``type_traits.__remove_alias`` function, by introducing
   small example that reproduced the error.

2. Huge speed improvement has been achieved (x10). Allen Bierbaum suggested to
   save and reuse results of different pygccxml algorithms:

   * ``declarations.remove_alias``
   * ``declarations.full_name``
   * ``declarations.access_type``
   * ``declarations.demangled_name``
   * ``declarations.declaration_path``

3. Interface changes:

  * ``declarations.class_t``:

    + ``set_members`` method was removed

    + ``adopt_declaration`` method was introduced, instead of ``set_members``

  * ``declarations.array_t`` class "set" accessor for size property was added.

  * ``declarations.namespace_t.adopt_declaration`` method was added.

  * ``declarations.variable_t.access_type`` property was added.

4. New type traits have been added:

   * ``is_same_function``

5. Few bug were fixed.

6. Documentation was improved.

Version 0.8.1
-------------

1. pygccxml has been ported to MacOS X. Many thanks to Darren Garnier!

2. New type traits have been added:

   * ``enum_traits``

   * ``class_traits``

   * ``class_declaration_traits``

   * ``is_std_string``

   * ``is_std_wstring``

   * ``remove_declarated``

   * ``has_public_less``

   * ``has_public_equal``

   * ``has_public_binary_operator``

   * ``smart_pointer_traits``

   * ``list_traits``

   * ``deque_traits``

   * ``queue_traits``

   * ``priority_queue``

   * ``vector_traits``

   * ``stack_traits``

   * ``map_traits``

   * ``multimap_traits``

   * ``hash_map_traits``

   * ``hash_multimap_traits``

   * ``set_traits``

   * ``hash_set_traits``

   * ``multiset_traits``

   * ``hash_multiset_traits``

3. ``enumeration_t`` class interface was changed. Enumeration values are kept
   in a list, instead of a dictionary. ``get_name2value_dict`` will build for
   you dictionary, where key is an enumeration name, and value is an enumeration
   value.

   This has been done in order to provide stable order of enumeration values.

4. Now you can pass operator symbol, as a name to query functions:

  .. code-block:: python

     cls = global_namespace.class_( 'my_class' )
     op = cls.operator( '<' )
     #instead of
     op = cls.operator( symbol='<' )

5. pygccxml improved a lot functionality related to providing feedback to user:

   * every package has its own logger

   * only important user messages are written to ``stdout``

   * user messages are clear

6. Support to Java native types has been added.

7. It is possible to pass an arbitrary string as a parameter to GCC_XML.

8. Native java types has been added to fundamental types.

9. Cache classes implementation was improved.

10. Few bug were fixed.

11. Documentation was improved.

12. ``mdecl_wrapper_t.decls`` property was renamed to  ``declarations``.
    The reason is that the current name ( ``decls`` ) conflicts with the method
    of the same name in the decl interface from ``declarations.scopedef_t`` class.

    So for example:

    .. code-block:: python

      classes = ns.decls("class")
      classes.decls("method")

    This will fail because it finds the attribute decls which is not a callable.

Version 0.8
-----------

1. pygccxml now has power "select" interface. Read more about this cool feature
   in tutorials.

2. Improved support for template instantiations. pygccxml now take into
   account demangled name of declarations. Please refer to documentation for
   more explanantion.

3. ``dummy_type_t`` - new type in types hierarchy. This is a very useful class
   for code generation projects.

4. New function - ``get_global_namespace``. As you can guess, it will find and
   return reference to global namespace.

5. New functionality in ``type_traits`` - ``has_public_assign``. This function
   will return True, if class has public assign operator.

6. ``declarations.class_t`` has new property - ``aliases``. This is a list of
   all class aliases.

7. Bug fixes.

8. Documentation has been updated/written/improved.

Version 0.7.1
-------------

**Attention - this going to be last version that is tested with Python 2.3**

1. New fundamental types has been added

   * complex float

   * complex double

   * complex long double

2. **Attention - non backward compatible change**

   ``declarations.filtering.user_defined`` and ``declarations.filtering.by_location``
   implementation has been changed. In previous version of those functions,
   ``decls`` list has been changed in place. This was wrong behavior. Now,
   those functions will return new list, which contains all desired declarations.

3. Few new type traits has been added

   * *type_traits.has_destructor*

   * *type_traits.has_public_destructor*

   * *type_traits.has_public_constructor*

   * *type_traits.is_noncopyable*

4. ``decl_printer_t`` class and ``print_declarations`` function have been added.
   Now you can print in a nice way your declaration tree or part of it.
   Thanks to Allen Bierbaum!

5. New class ``declarations.decl_factory_t`` has been added. This is a default
   factory for all declarations. From now all relevant parser classes takes as
   input instance of this class or ``Null``. In case of ``Null`` instance of
   ``declarations.decl_factory_t`` will be created. Using this class you can
   easily extend functionality provided by built-in declarations.

6. Sometimes, there is a need to find a declaration that match some criteria.
   The was such functionality in pygccxml, but it was too limited. This
   release fix the situation. pygccxml adds a set of classes that will help
   you to deal with this problem.

7. New cache - ``parser.directory_cache_t`` has been implemented.
   ``parser.directory_cache_t`` uses individual files stored in a dedicated
   cache directory to store the cached contents.
   Thanks to Matthias Baas!

8. ``parser.file_cache_t`` has been improved a lot.
   Thanks to Allen Bierbaum!

9. New file configuration is available: "cached source file".
   ``parser.project_reader_t`` class will check for existence of GCC_XML
   generated file. If it does not exist it will create one. If it do exist,
   then the parser will use that file.

10. Few helper functions has been added in order to make construction of
    configuration file to be as easy as possible:

    * ``parser.create_text_fc`` - creates file configuration, that contains text
    * ``parser.create_source_fc`` - creates file configuration, that contains
      reference to regular source file
    * ``parser.create_gccxml_fc`` - creates file configuration, that contains
      reference to GCC_XML generated file
    * ``parser.create_cached_source_fc`` - creates file configuration, that
      contains reference to 2 files: GCC_XML generated file and regular source
      file

11. Small bug fixes.

12. Documentation. Allen Bierbaum and Matthias Baas contributed so much in this
    area. Almost every public function/class has now documentation string.

13. Logging functionality has been added. pygccxml creates new logger
    "pygccxml". Now it is possible to see what pygccxml is doing right now.

14. I am sure I forgot something.

Version 0.6.9
-------------

1. New functions:

   * *type_traits.is_void_pointer*

   * *type_traits.array_size*

   * *type_traits.array_item_type*

2. Class *declarations.variable_t* has new property - *bit_fields*

3. Now it is possible to specify "undefined" directives using
   *parser.config_t* class.

4. *patch* functionality has been introduced. GCC_XML generates wrong
   default values for function arguments. *patch* functionality tries to fix
   this.

5. Small bug fixes

Version 0.6.8
-------------

1. Small bug has been fixed.

Version 0.6.7
-------------

1. New functions:

   * *type_traits.remove_pointer*

   * *type_traits.base_type*

   * *type_traits.is_convertible*

2. A lot of small bug fixes.

3. Few English mistakes have been fixed.

   .. attention::

      There are 2 none backward compatible changes:

      * class with name **compaund_t** has been renamed to **compound_t**

      * word **pathes** has been replaced with **paths**

4. There are new properties on

   * *declarations.declaration_t.top_parent*

   * *declarations.class_t.recursive_bases* returns all base classes of the
     class

   * *declarations.class_t.recursive_derived* returns all derived classes of
     the class

   * *member_calldef_t.access_type*

5. New type has been introduced: *unknown_t*. There are use cases when
   GCC_XML does not returns function return type.

6. New implementation of *make_flatten* algorithm using generators.
   By default old implementation will be used.

7. *parser.file_configuration_t* interface has been changed. Now it is able
   to keep: source file, text or GCC_XML generated file. If you are doing
   something with code that is not changing you'd better use GCC_XML
   generated file as content of the *parser.file_configuration_t*. Save your
   time.

8. There are some cases when GCC_XML reports *"restricted"*. In this case
   pygccxml replaces *"restricted"* with *"volatile"*.
