=========================================
GCC-XML 0.7 → 0.9 upgrade issues (Legacy)
=========================================

------------
Introduction
------------

This page is kept here for historical reasons. CastXML is the recommended
xml generator and GCC-XML is being phased out. This page will be removed
in version 2.0.0 of pygcxml.

Recently, GCC-XML internal parser was updated to GCC 4.2. The internal representation
of source code, provided by GCC's parser, has changed a lot and few backward
compatibility issues were introduced. In this document, I will try to cover all
problems you may encounter.


-------------------
Default constructor
-------------------

GCC-XML 0.9 doesn't report compiler generated default and copy constructors as
an implicit ones.

If you rely heavily on their existence in the generated XML, I suggest you to switch
to :func:`has_trivial_constructor <pygccxml.declarations.type_traits.has_trivial_constructor>`
and to :func:`has_trivial_copy <pygccxml.declarations.type_traits.has_copy_constructor>` functions.

--------------------------
Pointer to member variable
--------------------------

Previous version of GCC-XML reported pointer to member variable as a "PointerType"
with reference to "OffsetType". The new version removes "PointerType" from this sequence.

C++ code:

.. code-block:: c++

  struct xyz_t{
    int do_smth( double );
    int m_some_member;
  };

  typedef int (xyz_t::*mfun_ptr_t)( double );

  typedef int (xyz_t::*mvar_ptr_t);

GCC-XML 0.7:

.. code-block:: xml

  <Typedef id="_6" name="mfun_ptr_t" type="_5" />
  <PointerType id="_5" type="_128" size="32" align="32"/>
  <MethodType id="_128" basetype="_7" returns="_136">
    <Argument type="_140"/>
  </MethodType>

  <Typedef id="_4" name="mvar_ptr_t" type="_3" />
  <PointerType id="_3" type="_127" size="32" align="32"/>
  <OffsetType id="_127" basetype="_7" type="_136" size="32" align="32"/>

GCC-XML 0.9:

.. code-block:: xml

  <Typedef id="_97" name="mfun_ptr_t" type="_96" />
  <PointerType id="_96" type="_147" size="32" align="32"/>
  <MethodType id="_147" basetype="_92" returns="_131">
    <Argument type="_127"/>
  </MethodType>

  <Typedef id="_52" name="mvar_ptr_t" type="_139" />
  <OffsetType id="_139" basetype="_92" type="_131" size="32" align="32"/>

pygccxml handles this issue automatically, you don't have to change your code.

-----------------------
Constant variable value
-----------------------

GCC-XML 0.9 uses suffix to report the constant variable value

For example:

.. code-block:: c++

  const long unsigned int initialized = 10122004;

GCC-XML 0.9 will report the ``initialized`` value as ``10122004ul``, while GCC-XML
0.7 as ``10122004``.

pygccxml handles  this problem automatically, you don't have to change your code.

------------------------------------------
Free and member function default arguments
------------------------------------------

Both versions of GCC-XML have a few issues, related to default arguments. GCC-XML 0.9
fixes some issues, but introduces another ones. Take a look on the following examples:

* Example 1

  .. code-block:: c++

    void fix_numeric( ull arg=(ull)-1 );

  GCC-XML 0.7

  .. code-block:: xml

    <Argument name="arg" type="_7" default="0xffffffffffffffff"/>


  GCC-XML 0.9

  .. code-block:: xml

    <Argument name="arg" type="_103" default="0xffffffffffffffffu"/>

* Example 2

  .. code-block:: c++

    void fix_function_call( int i=calc( 1,2,3) );

  GCC-XML 0.7

  .. code-block:: xml

    <Argument name="i" type="_9" default="function_call::calc(int, int, int)(1, 2, 3)"/>


  GCC-XML 0.9

  .. code-block:: xml

    <Argument name="i" type="_34" default="function_call::calc(1, 2, 3)"/>

* Example 3

  .. code-block:: c++

    void typedef__func( const typedef_::alias& position = typedef_::alias() );

  GCC-XML 0.7

  .. code-block:: xml

    <Argument name="position" type="_1458" default="alias()"/>


  GCC-XML 0.9

  .. code-block:: xml

    <Argument name="position" type="_1703" default="typedef_::original_name()"/>

* Example 4

  .. code-block:: c++

    void typedef__func2( const typedef_::alias& position = alias() );

  GCC-XML 0.7

  .. code-block:: xml

    <Argument name="position" type="_1458" default="alias()"/>


  GCC-XML 0.9

  .. code-block:: xml

    <Argument name="position" type="_1703" default="typedef_::original_name()"/>


* Example 5

  .. code-block:: c++

    node* clone_tree( const std::vector<std::string> &types=std::vector<std::string>() );

  GCC-XML 0.7

  .. code-block:: xml

    <Argument name="types" type="_3336" default="vector&lt;std::basic_string&lt;char, std::char_traits&lt;char&gt;, std::allocator&lt;char&gt; &gt;,std::allocator&lt;std::basic_string&lt;char, std::char_traits&lt;char&gt;, std::allocator&lt;char&gt; &gt; &gt; &gt;((&amp;allocator&lt;std::basic_string&lt;char, std::char_traits&lt;char&gt;, std::allocator&lt;char&gt; &gt; &gt;()))"/>


  GCC-XML 0.9

  .. code-block:: xml

    <Argument name="types" type="_3096" default="std::vector&lt;std::basic_string&lt;char, std::char_traits&lt;char&gt;, std::allocator&lt;char&gt; &gt;, std::allocator&lt;std::basic_string&lt;char, std::char_traits&lt;char&gt;, std::allocator&lt;char&gt; &gt; &gt; &gt;(((const std::allocator&lt;std::basic_string&lt;char, std::char_traits&lt;char&gt;, std::allocator&lt;char&gt; &gt; &gt;&amp;)((const std::allocator&lt;std::basic_string&lt;char, std::char_traits&lt;char&gt;, std::allocator&lt;char&gt; &gt; &gt;*)(&amp; std::allocator&lt;std::basic_string&lt;char, std::char_traits&lt;char&gt;, std::allocator&lt;char&gt; &gt; &gt;()))))"/>

Basically pygccxml can't help you here. The good news is that you always can
change the default value expression from the script:

.. code-block:: python

  #f is "calldef_t" instance
  for arg in f.arguments:
      arg.default_value = <<<new default value or None>>>


-------------
Name mangling
-------------

GCC-XML 0.9 mangles names different than the previous one. This change is the most
dramatic one, because it may require from you to change the code.

Consider the following C++ code:

.. code-block:: c++

  template< unsigned long i1>
  struct item_t{
    static const unsigned long v1 = i1;
  };

  struct buggy{
    typedef unsigned long ulong;
    typedef item_t< ulong( 0xDEECE66DUL ) | (ulong(0x5) << 32) > my_item_t;
    my_item_t my_item_var;
  };

====================  ======================  =======================
    generated data         GCC-XML 0.7             GCC-XML 0.9
====================  ======================  =======================
class name            item_t<0x0deece66d>     item_t<-554899859ul>
class mangled name    6item_tILm3740067437EE  6item_tILm3740067437EE
class demangled name  item_t<3740067437l>     item_t<3740067437ul>
====================  ======================  =======================

pygccxml uses class demangled name as a "name" of the class. This was done to
overcome few bugs GCC-XML has, when it works on libraries with extreme usage of
templates.

As you can see the name of the class is different. pygccxml is unable to help
you in such situations. I suggest you to use query API strict mode. This is the
default one. If the class/declaration with the given name could not be found, it
will raise an error with clear description of the problem.

You can also to print the declarations tree to ``stdout`` and find out the name
of the class/declaration from it.



.. _`Python`: http://www.python.org
.. _`GCC-XML`: http://www.gccxml.org
