======================
Declarations query API
======================

------------
Introduction
------------
You parsed the source files. Now you have to do some real work with the extracted
information, right? pygccxml provides very powerful and simple interface to
query about extracted declarations.

Just an example. I want to select all member functions, which have 2 arguments.
I don't care about first argument type, but I do want second argument type to be
a reference to an integer. More over, I want those functions names to end with
"impl" string and they should be protected or private.

.. code-block:: python

  #global_ns is the reference to an instance of namespace_t object, that
  #represents global namespace
  query = declarations.custom_matcher_t( lambda mem_fun: mem_fun.name.endswith( 'impl' )
  query = query & ~declarations.access_type_matcher_t( 'public' )
  global_ns.member_functions( function=query, arg_types=[None, 'int &'] )

The example is complex, but still readable. In many cases you will find
yourself, looking for one or many declarations, using one or two declaration properties.
For example:

.. code-block:: python

  global_ns.namespaces( 'details' )

This call will return all namespaces with name 'details'.

--------------
User interface
--------------

As you already know, ``pygccxml.declarations`` package defines the following classes:

* :class:`scopedef_t <pygccxml.declarations.scopedef.scopedef_t>` - base class
  for all classes, that can contain other declarations

* :class:`namespace_t  <pygccxml.declarations.namespace.namespace_t>` - derives
  from :class:`scopedef_t <pygccxml.declarations.scopedef.scopedef_t>` class,
  represents C++ namespace

* :class:`class_t  <pygccxml.declarations.class_declaration.class_t>` - derives
  from :class:`scopedef_t <pygccxml.declarations.scopedef.scopedef_t>` class,
  represents C++ class/struct/union.

So, the query methods defined on ``scopedef_t`` class could be used on instances
of ``class_t`` and ``namespace_t`` classes. I am sure you knew that.

Usage examples
--------------

I will explain the usage of ``member_function`` and ``member_functions`` methods.
The usage of other methods is very similar to them. Here is definition of those
methods:

.. code-block:: python

  def member_function(  self,
                        name=None,
                        function=None,
                        return_type=None,
                        arg_types=None,
                        header_dir=None,
                        header_file=None,
                        recursive=None )

  mem_fun = member_function #just an alias

  def member_functions( self,
                        name=None,
                        function=None,
                        return_type=None,
                        arg_types=None,
                        header_dir=None,
                        header_file=None,
                        recursive=None,
                        allow_empty=None )
  mem_funs = member_functions


As you can see, from the method arguments you can search for member function
by:

  * ``name``

    Python string, that contains member function name or full name.

    .. code-block:: python

      do_smth = my_class.member_function( 'do_smth' )
      do_smth = my_class.member_function( 'my_namespace::my_class::do_smth' )

  * ``function``

    Python callable object. You would use this functionality, if you need to
    build custom query. This object will be called with one argument - declaration,
    and it should return ``True`` or ``False``.

    .. code-block:: python

      impls = my_class.member_functions( lambda decl: decl.name.endswith( 'impl' ) )


    ``impls`` will contain all member functions, that their name ends with "impl".

  * ``return_type``

    the function return type. This argument can be string or an object that describes
    C++ type.

    .. code-block:: python

      mem_funcs = my_class.member_functions( return_type='int' )

      i = declarations.int_t()
      ref_i = declarations.reference_t( i )
      const_ref_i = declarations.const_t( ref_i )
      mem_funcs = my_class.member_functions( return_type=const_ref_int )

  * ``arg_types``

    Python list that contains description of member function argument types.
    This list could be a mix of Python strings and objects that describes C++
    type. Size of list says how many arguments function should have. If you want
    to skip some argument type from within comparison, you put ``None``, into
    relevant position within the list.

    .. code-block:: python

      mem_funcs = my_class.member_functions( arg_types=[ None, 'int'] )

    ``mem_funcs`` will contain all member functions, which have two arguments
    and type of second argument is ``int``.

  * ``header_dir``

    Python string, that contains full path to directory, which contains file,
    which contains the function declaration

    ``mem_funcs = my_namespace.member_functions( header_dir='/home/roman/xyz' )``

  * ``header_file``

    Python string, that contains full path to file, which contains the function
    declaration.

    ``mem_funcs = my_namespace.member_functions( header_dir='/home/roman/xyz/xyz.hpp' )``

  * ``recursive``

    Python boolean object.

    If ``recursive`` is ``True``, then member function will be also searched
    within internal declarations.

    If ``recursive`` is ``False``, then member function will be searched only
    within current scope.

    What happen if ``recursive`` is ``None``? Well. ``scopedef_t`` class defines
    ``RECURSIVE_DEFAULT`` variable. Its initial value is ``True``. So, if you
    don't pass ``recursive`` argument, the value of ``RECURSIVE_DEFAULT`` variable
    will be used. This "yet another level of indirection" allows you to configure
    pygccxml "select" functions in one place for all project.

  * ``allow_empty``

    Python boolean object, it says pygccxml what to do if query returns empty.

    If ``allow_empty`` is ``False``, then exception
    ``RuntimeError( "Multi declaration query returned 0 declarations." )``
    will be raised

    ``allow_empty`` uses same technique as ``recursive``, to allow you to customize
    the behavior project-wise. The relevant class variable name is
    ``ALLOW_EMPTY_MDECL_WRAPPER``. Its initial value is ``False``.

Now, when you understand, how to call those functions, I will explain what they
return.

``member_function`` will always return reference to desired declaration. If
declaration could not be found or there are more then one declaration that
match query ``RuntimeError`` exception will be raised.

Return value of ``member_functions`` is not Python list or set, but instance
of ``mdecl_wrapper_t`` class. This class allows you to work on all selected
objects at once. I will give an example from another project - https://pypi.python.org/pypi/pyplusplus/.
In order to help `Boost.Python`_ to manage objects life time, all functions
should have `call policies`_. For example:

.. code-block:: c++

  struct A{
      A* clone() const { return new A(); }
      ...
  };

.. code-block:: c++

  struct B{
      B* clone() const { return new B(); }
      ...
  };

``clone`` member function `call policies`_ is ``return_value_policy<manage_new_object>()``.
The following code applies the `call policies`_ on all ``clone`` member functions within the
project:

.. code-block:: python

  #global_ns - instance of namespace_t class, that contains reference to global namespace
  clone = global_ns.member_functions( 'clone' )
  clone.call_policies = return_value_policy( manage_new_object )


Another example, from https://pypi.python.org/pypi/pyplusplus/ project. Sometimes it is desirable to
exclude declaration, from being exported to Python. The following code will exclude
``clone`` member function from being exported:

.. code-block:: python

  global_ns.member_functions( 'clone' ).exclude()

As you can see this class allows you to write less code. Basically using this
class you don't have to write loops. If will do it for you. Also if you insist to
write loops, ``mdecl_wrapper_t`` class implements ``__len__``, ``__getitem__``
and ``__iter__`` methods. So you can write the following code:

.. code-block:: python

  for clone in global_ns.member_functions( 'clone' ):
      print clone.parent.name


----------------------
Implementation details
----------------------

Performance
-----------

For big projects, performance is critical. When you finished to build/change
declarations tree, then you can call ``scopedef_t.init_optimizer`` method.
This method will initialize few data structures, that will help to minimize the
number of compared declarations. The price you are going to pay is memory usage.

Data structures
~~~~~~~~~~~~~~~
Here is a short explanation of what data structures is initialized.

* ``scopedef_t._type2decls``, ``scopedef_t._type2decls_nr``

  Python dictionary, that contains mapping between declaration type and
  declarations in the current scope.

  ``scopedef_t.type2decls_nr`` contains only declaration from the current scope.
  ``scopedef_t.type2decls`` contains declarations from the current scope and its children

* ``scopedef_t._type2name2decls``, ``scopedef_t._type2name2decls_nr``

  Python dictionary, that contains mapping between declaration type and
  another dictionary. This second dictionary contains mapping between
  a declaration name and declaration.

  ``scopedef_t.type2name2decls_nr`` contains only declaration from the current scope.
  ``scopedef_t.type2name2decls`` contains declarations from the current scope and its children

* ``scopedef_t._all_decls``

  A flat list of all declarations, including declarations from the children scopes.

Except ``scopedef_t.decl`` and ``scopedef_t.decls`` methods, all other queries
have information about declaration type.

If you include ``name`` into your query, you will get the best performance.

----------------
More information
----------------

I think, I gave you the important information. If you need definition of some
query method, you can take a look on API documentation or into source code.


.. _`Boost.Python`: http://boost.org/libs/python/doc/tutorial/doc/html/index.html
.. _`call policies`: http://boost.org/libs/python/doc/tutorial/doc/html/python/functions.html#python.call_policies
.. _`Call policies`: http://boost.org/libs/python/doc/tutorial/doc/html/python/functions.html#python.call_policies

.. _`Python`: http://www.python.org
.. _`GCC-XML`: http://www.gccxml.org
.. _`UML diagram` : declarations_uml.png
.. _`parser package UML diagram` : parser_uml.png
.. _`boost::type_traits` : http://www.boost.org/libs/type_traits/index.html
