# =============================================================================
#
#  Copyright 2014 Insight Software Consortium
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0.txt
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# =============================================================================

# Copyright 2004-2013 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

"""
defines default declarations factory class
"""

from .calldef import member_function_t
from .calldef import constructor_t
from .calldef import destructor_t
from .calldef import member_operator_t
from .calldef import casting_operator_t
from .calldef import free_function_t
from .calldef import free_operator_t
from .enumeration import enumeration_t
from .namespace import namespace_t
from .class_declaration import class_t
from .class_declaration import class_declaration_t
from .typedef import typedef_t
from .variable import variable_t


class decl_factory_t(object):

    """
    declarations factory class
    """

    def __init__(self):
        """creates declarations factory"""
        object.__init__(self)

    def create_member_function(self, *arguments, **keywords):
        """creates instance of class that describes member function
        declaration"""
        return member_function_t(*arguments, **keywords)

    def create_constructor(self, *arguments, **keywords):
        """creates instance of class that describes constructor declaration"""
        return constructor_t(*arguments, **keywords)

    def create_destructor(self, *arguments, **keywords):
        """creates instance of class that describes destructor declaration"""
        return destructor_t(*arguments, **keywords)

    def create_member_operator(self, *arguments, **keywords):
        """creates instance of class that describes member operator
        declaration"""
        return member_operator_t(*arguments, **keywords)

    def create_casting_operator(self, *arguments, **keywords):
        """creates instance of class that describes casting operator
        declaration"""
        return casting_operator_t(*arguments, **keywords)

    def create_free_function(self, *arguments, **keywords):
        """creates instance of class that describes free function
        declaration"""
        return free_function_t(*arguments, **keywords)

    def create_free_operator(self, *arguments, **keywords):
        """creates instance of class that describes free operator
        declaration"""
        return free_operator_t(*arguments, **keywords)

    def create_class_declaration(self, *arguments, **keywords):
        """creates instance of class that describes class declaration"""
        return class_declaration_t(*arguments, **keywords)

    def create_class(self, *arguments, **keywords):
        """creates instance of class that describes class definition
        declaration"""
        return class_t(*arguments, **keywords)

    def create_enumeration(self, *arguments, **keywords):
        """creates instance of class that describes enumeration declaration"""
        return enumeration_t(*arguments, **keywords)

    def create_namespace(self, *arguments, **keywords):
        """creates instance of class that describes namespace declaration"""
        return namespace_t(*arguments, **keywords)

    def create_typedef(self, *arguments, **keywords):
        """creates instance of class that describes typedef declaration"""
        return typedef_t(*arguments, **keywords)

    def create_variable(self, *arguments, **keywords):
        """creates instance of class that describes variable declaration"""
        return variable_t(*arguments, **keywords)
