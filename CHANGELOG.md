Changes
=======

Version 2.1.0 (unreleased)
--------------------------

Version 2.0.1
-------------

1. Minor description and doc updates for release uploads

Version 2.0.0
-------------

1. Drop support for ```GCC-XML```.

  * Drop all the demangled name attributes

  * Drop declarations.class_t.USE_DEMANGLED_AS_NAME

2. Drop support for ```Python 2.6```, ```Python 2.7```, ```Python 3.2```, ```Python 3.3```, ```Python 3.4```.

3. Add support for ```Python 3.5```, ```Python 3.6```, ```Python 3.7```, ```Python 3.8```.

4. Deprecated all the `i_depend_on_them` methods from the `declaration_t`
   class hierarchy. Instead of using `decl.i_depend_on_them()`, please use the
   `declarations.get_dependencies_from_decl(decl)` function from the
   `declarations` module, which returns the same result.

5. Add support for `-std=c++17` and `-std=c++2a` flags

6. Add `g++` and `gcc` to better support gnu compilers on windows

Version 1.9.1
-------------

1. Fix bug in the ```find_noncopyable_vars``` method which wrongly returned
   member variables of pointer type (#84)

2. Fix bug in the ```smart_pointer_traits.value_type``` and
   ```auto_pointer_traits.value_type``` methods which didn't find the expected
   ```value_type``` declaration (#85)

3. Fix bug in the ```smart_pointer_traits.is_smart_pointer``` and
   ```auto_pointer_traits.is_smart_pointer``` methods which didn't properly
   work (#85)

Version 1.9.0
-------------

1. [New features]

  * Full Python 3.6 support

  * Full pypy and pypy3 support

  * Better windows support

  * Small performance improvements

  * Added ```is_struct``` function to declarations package. It returns true if
    a declaration is a struct.

  * Added support for the castxml epic version format 1.
    This is a new format which is partially not backward compatible with the
    legacy format. To use this new format, use the ```castxml_epic_version``` flag
    and set it to 1.
    This new format will allow to support new c++ features that were not recognized
    by ```gccxml``` and previous versions of ```castxml```.

  * Added support for elaborated type specifiers.
    A new ```elaborated_t``` type was added, with the related ```is_elaborated```
    and ```remove_elaborated``` function.
    This is only available when setting the ```castxml_epic_version``` flag to 1 .

2. [Windows]

  * Add Appveyor Windows build (castxml, VS 2013, python 3.5) and merge coverage
    results with Travis.

  * Attributes defined as ```__thiscall__``` are now ignored (tested with VS 2013).
    The ```__thiscall__``` in some attributes will be removed too. If you still
    want to have access to these attributes, you can use the
    ```config.flags = ["f2"]``` option.

3. [Deprecations]

  * Deprecated ```decl``` attribute from ```dependency_info_t```.
    Use the ```declaration``` attribute instead.

  * Deprecated the ```nss```, ```free_fun``` and ```free_funs``` methods from the
    ```namespace_t``` class. Use the ```namespaces```, ```free_function``` and
    ```free_functions``` methods instead.

  * Deprecated the ```mem_fun```, ```mem_funs```, ```mem_oper```, ```mem_opers```,
    ```enum``` and ```enums``` methods from the ```scopedef_t``` class.
    Use the ```member_function```, ```member_functions```, ```member_operator```,
    ```member_operators```, ```enumeration``` and ```enumerations``` methods instead.

  * Deprecated the ```mdecl_wrapper_t.to_list()```. You can implement your own
      version of it if you really need it.

  * Deprecated the ```declaration_not_found_t``` and ```multiple_declarations_found_t```
    attributes from the ```scopedef_t``` class. These exceptions are available
    through the ```pygccxml.declarations``` package.

  * Deprecated the ```decorated_name``` attribute from ```declaration_t```.
    This was used by the binary parser, which have been removed in this version.
    As these attributes still could be used somewhere (but always returned None
    anyway), they need to go through a deprecation cycle first.

4. [Removals]

  * Removed ```utils.xml_generator``` and ```utils.xml_output_version``` attributes.
    These two variables should not have made it into the public API. There is no
    deprecation cycle for these because of the complexity of keeping these
    module attributes around.

Version 1.8.6
-------------

1. Fix _HAS_TR1=0 definition for msvc9 (#72)

2. Fix possible infinite recursion in ```find_noncopyable_vars()``` (#71)

Version 1.8.5
-------------

1. Fix multiple calls to ``` __hash__()``` (#70)

2. ```Static``` and ```extern``` qualifiers are now no more treated as equivalents
    in the type_qualifiers class (for ```CastXML```).
    The old behaviour is kept for ```GCC-XML``` (```static == extern```).

3. Fix for ```declarations.is_noncopyable``` when used on a ```pointer_t```.

Version 1.8.4
-------------

1. Include paths read from configuration files on windows are now normed
   and passed between quotation marks. This makes ```pygccxml``` more robust
   when used on Windows (with paths containing whitespaces).

2. Closed cache file handle, which would not be closed in case of an exception
   (warning thrown by Python 2.7.13)

3. Always call wait() on subprocesses before closing stdout/stderr streams.
   Detected by Python 3.6. Fixes the following warning:
   ResourceWarning: subprocess xxxxx is still running

4. Fix deprecation warnings thrown by ```ConfigParser``` when using pygccxml
   with python 2.7.13. Fix the usage of ```pygccxml``` with python 3.6.

5. Updated travis setup to python 3.6 for OS X.

Version 1.8.3
-------------

1. Single-source the version number to prevent version numbers mismatches.
   Release 1.8.2 contained a wrong version number in its download url
   on pypi.


Version 1.8.2
-------------

1. ```xml_generator_configuration_t``` will no more try to find
  castxml or gccxml. You can use ```utils.find_xml_generator``` to help you
  finding the path to the xml generator, or set it manually.
  It is now mandatory to pass a valid ```xml_generator``` and
  ```xml_generator_path``` to the configuration (#65).

Version 1.8.1
-------------

1. Added ```is_struct``` function to declarations package. It returns true if
  a declaration is a struct.

2. Removed * from decl_string when type is a function pointer (#61)

3. Update travis.yml for newer OS X images. Update CastXML binaries for Travis.

4. Fix regression in directory_cache, which was crashing due an unset variable.
  Add support for python3 in directory_cache.

Version 1.8.0
-------------

1. ```CastXML``` is now the default XML generator (instead of ```GCCXML```)
   ```find_xml_generator``` will now look for ```CastXML``` first too.

2. Do not allow to use the GCCXML provided by newer gccxml debian packages.
  It is a wrapper around CastXML which can confuse pygccxml.
  You should use the castxml package and the CastXML binary instead.
  If you really want to use gccxml, the gccxml.real binary from the
  gccxml debian package can still be used.

3. Fix parsing of ```boost/locale.hpp``` code.
  Templated class instantiations with specializations are now better supported,
  specifically when containing parentheses:
  ```myClass<std::vector<char>(const std::string &, const std::string &)> obj;```

4. When using the ```remove_pointer``` function on a function pointer, the
  ```remove_pointer``` function now correctly returns a ```calldef_type_t```.

5. ```declarations.is_string```, ```declarations.is_std_wstring```,
  ```declarations.is_std_ostream``` and ```declarations.is_std_wostream``` now
  correctly work when a the type is also a reference.
  Example: ```declarations.is_string``` returned false for
  ```typedef std::string& x3;```; it will return true now.

6. General code style overhaul (with the help of quantifiedcode.com)

7. Added a bunch of new examples and documentation update and cleanup

8. [Removals] Remove ```compiler``` attribute in declarations.py and
   ```gccxml_path``` from config.py
  These were deprecated in pygccxml v1.7.0, and definitively removed for v1.8.0

9. [Deprecations]
  * The ```binary_parsers``` module was deprecated. It seems that this module is not
    used by other third-party projects, at least a quick search on GitHub
    did not give any interesting usage. Also, this code is not tested, and
    there seem to be some undefined variables, so it is highly probable that this
    module is not working anyway.
    I do not want to put much efforts in maintaining this module, but concentrate
    on improving pygccxml's core features. If somebody wants to revive this
    module it can still be done in a separate project.
    Thus, the 3 following functions are now deprecated and will be removed in
    pygccxml 1.9.0: ```merge_information```, ```undecorate_blob``` and ```format_decl```.
    The ```undname_creator_t``` class is also deprecated for the same reason.

  * A bunch of attributes and methods were deprecated.
   They will throw a warning when used with pygccxml 1.8.0, and will be removed
   in version 1.9.0.
     * In ```class_declaration_t``` and ```class_t```:
       - decl.container_traits attribute => declarations.find_container_traits(decl)
     * In ```class_t```
       - decl.find_noncopyable_vars() method => declarations.find_noncopyable_vars(decl)
       - decl.find_copy_constructor() method => declarations.find_copy_constructor(decl)
       - decl.has_vtable argument => declarations.has_vtable(decl)
     * In ```constructor_t```
       - ctor.is_copy_constructor attribute  => declarations.is_copy_constructor(ctor)
       - ctor.is_trivial_constructor attribute => declarations.is_trivial_constructor(ctor)

     * Deprecate the ```ns()``` method. The ```namespace()``` method can be used instead.

     * Deprecate ```etree_scanner_t``` and ```etree_saxifier_t``` classes.
       The most efficient xml scanner class is the ```ietree_scanner_t``` class, which
       is the one used since many years now.

     * The ```[gccxml]``` section used in the configuration file is now deprecated.
       Please use ```[xml_generator]``` instead.

  * ```native_compiler``` and ```enum``` classes from the ```utils``` module. These were
     not used in ```pygccxml```, and can easily be implemented in your own project if you
     need and equivalent


Version 1.7.6
-------------

1. Fix problem with argument without names when building declaration string (#55)

Version 1.7.5
-------------

1. Improve error message when no castxml or gccxml is found.

2. Fix compilation of tests with c++11.

3. Fix patching of enums in default arguments for C++03.

4. Version numbers are still tagged with the v prefix (1.7.4 was correctly tagged),
   as this is recommended by GitHub. The version number in the __init__.py and
   setup.py files are without v prefix, because this is what pip requires.

Thanks to the following people for their contribution to this release:
Ashish Sadanandan

Version 1.7.4
-------------

1. CV-qualified arrays were not being handled correctly by type traits
   manipulations functions. For instance, 'int const[N]' would not be
   detected as 'const'. Similar problems existed for volatile qualified
   arrays too. See #35 for more details. A newer version of CastXML is
   recommended (xml output version >= 1.138)

2. Close subprocess stdout stream once value has been read.
   Fixes some warnings under python3.

3. Since this release, pyggcxml's version numbers do not contain the ``v``
   prefix anymore. This was breaking distribution on PyPI (pypi.python.org).

4. The documentation is now at http://pygccxml.readthedocs.io/

Thanks to the following people for their contribution to this release:
Ashish Sadanandan

Version 1.7.3
-------------

1. Addition of an is_union() method in the type_traits module.

2. type_traits.smart_pointer_traits will now classify std::shared_ptr as a
   smart pointer (only boost::shared_ptr was recognized before)

3. Fix a regression in undname_creator_t.format_argtypes

4. C++xx flags are now correctly passed to CastXML. Allowed flags are:
   "-std=c++98", "-std=c++03", "-std=c++11", "-std=c++14", "-std=c++1z"
   Thanks to Mark Moll for the fix.

5. Add better support for "typedef (class|struct) {} foo;" syntax when using
   CastXML. GCCXML did not recognize the typedef. Fetching these
   declarations can now be done with: .typedef("foo") or .class_("foo").

6. Add support for the future llvm 3.9. As in release v1.7.1, new structs and
   typedefs are now exposed by llvm, which broke pyplusplus.
   In this case these are ```__NSConstantString_tag``` and ```__NSConstantString```.
   The two declarations are now hidden from the declarations tree, but can still
   be generated by using the ```config.flags = ["f1"]``` option.

7. Multiple fixes to adapt default arguments in functions for py++. Using the
   latest version of CastXML is recommended. This makes sure default arguments
   for function parameters are correctly defined, so that py++ can process them.

8. Fix for exception when using castxml + gcc5 + std=c++11 and maps.

9. Removed unittest2 dependency for testing with python 2.6

10. Testing: test with std::tr1 unordered containers for gcc >= 4.4.7 and castxml

11. Cosmetic fix for generator name printed to stdout when launching unit tests

12. Fix simple typo in example.py comment

Thanks to the following people for their contribution to this release:
Mark Moll, Ashish Sadanandan, Mark Oates

Version 1.7.2
-------------

1. Fix exception in is_copy_constructor when the constructor's argument was
   a typedef. is_copy_constructor will now return False instead of failing.
   See issue #27.

2. Fix bug with utils.xml_generator being unset when reading cached file.
   This could for example happen when reading a cached file from a second
   python interpreter (e.g. in a subprocess or by calling pygccxml
   multiple times from a script). See issue #27.

3. SafeConfigParser is throwing a deprecation warning in python 3.2 and newer.
   Use ConfigParser instead. Thanks to Mark Moll for the patch.

4. Add support for cflags property in config files.
   Thanks to Mark Moll for the patch.

Version 1.7.1
-------------

1. Remove the __va_list_tag declaration from the tree when parsing with CastXML

   The __va_list_tag declarations are internal declarations, which are often
   not needed. They are for example polluting the declarations tree when running
   pyplusplus.

   This is optional but on by default. To still load the __va_list_tag declarations
   in the tree, a config flag can be set like this: ``config.flags = ["f1"]``,
   or by passing the ``flags=["f1"]`` argument the config setup.

2. Some code cleanup

3. Build new package for pypi. The ``1.7.0`` upload has gone wrong ...


Version 1.7.0
-------------

1. Added support for CastXML (https://github.com/CastXML/CastXML)

   GCCXML is deprecated and does no more work with modern compilers.
   CastXML should be used instead.

   ``pygccxml 1.7.0`` is still compatible with GCCXML and no changes are needed for people working with GCCXML.

2. [CastXML] A new function was introduced to help find which XML generator you are using.

   If the generator (GCCXML or CastXML) is in your path, it will be detected.

    .. code-block:: python

      generator_path, generator_name = pygccxml.utils.find_xml_generator()

3. [CastXML] When using the configuration, you will need to tell pygccxml which xml generator you are using.

    .. code-block:: python

      xml_generator_config = parser.xml_generator_configuration_t(
        xml_generator_path=generator_path,
        xml_generator=generator_name,
        )

  ``gccxml_configuration_t`` is an alias of ``xml_generator_configuration_t``.

  ``load_gccxml_configuration`` is an alias of ``load_xml_generator_configuration``.

  Both can still be used but will be deprecated.

4. [CastXML] The compiler path can be passed to castxml.

   This is done by using the ``compiler_path`` attribute in the configuration.
   Note that this may be important because the resulting xml file is slightly different
   depending on the compiler.

5. [CastXML] Added support for some fields which have no location.

   These fields are: ``gp_offset``, ``fp_offset``, ``overflow_arg_area``, ``reg_save_area``

6. [CastXML] Mangled names are only available for functions and variables with CastXML.

  Getting the mangled attribute on a ``declaration`` will fail.

7. [CastXML] Demangled names are not available.

  Getting a demangled name will fail.

8. [CastXML] Add new container traits:

  ``unordered maps``, ``unordered sets``, ``multimaps``, ``multisets``

9. [CastXML] Annotations:

  Instead of using the ``__attribute((gccxml("string")))`` c++ syntax (see version 0.9.5), the ``__attribute__ ((annotate ("out")))`` can now be used to annotate code with CastXML.

10. [CastXML] Disabled relinking of:

    .. code-block:: python

      rebind<std::__tree_node<std::basic_string<char>, void *> >

 This made the ``find_container_traits_tester`` unit tests fail with ``CastXML``.
 This class defintion is present in the clang AST tree, but I don't know why it is
 usefull. Please tell me if you need it so we can re-enable that featur in pygccxml.

11. [Misc] Deprecated the ``compiler`` attribute and replaced it with a global ``utils.xml_generator`` variable.

 The ``compiler`` attribute was misleading; it was sometimes confused with the name and version of the xml generator.

 This change also fixes some internal problems with the algorithms cache.

12. [Misc] ``declarations.has_trivial_copy`` was defintevely removed.

  Please use ``declarations.has_copy_constructor``.

  This was deprecated since version 0.9.5.

13. [Misc] Remove ``gccxml`` logger from logger class (was deprecated).

  Please use ``cxx_parser`` instead.

14. [Misc] Removed ``gccxml_runtime_error_t`` class. This was only used internally.

  Please use a normal ``RuntimeError`` instead.

15. [Misc] Documentation was moved to readthedocs.org

  https://readthedocs.org/projects/pygccxml/

16. [Misc] Add quantifiedcode check

  https://www.quantifiedcode.com/app/project/117af14ef32a455fb7b3762e21083fb3

17. [Misc] Add option to keep xml files after errors, which is useful for debugging purposes.

18. [Misc] Fix new pep8 warnings, clean up and simplify some code and comments

19. [Misc] The compiler version debugging message is now hidden (closes #12)

20. [Misc] Print less line separations in ``decl_printer``; this makes the output more compact.

21. [Tests] Add new test for the ``contains_parent_dir`` function.

22. [Tests] Add test for non copyable class with const class

23. [Tests] Add test case for non copyable class due to const array

24. [Doc] Small documentation update, moved people list to credits page, added new examples.

25. [Misc] Add Travis unit tests for Python 3.5


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

Note about version numbers before 1.5.0
---------------------------------------

When the project moved from svn to git, versions were tagged from 1.0.0 on.
Note that there was no 1.2, 1.3 nor 1.4 version (this is maybe due to the
many forks and the slow down of the maintenance effort).

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
