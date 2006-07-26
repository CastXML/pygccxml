# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import types
import algorithm

class matcher:
    
    class declaration_not_found_t( RuntimeError ):
        def __init__( self, matcher ):
            RuntimeError.__init__( self )
            self.matcher = matcher
            
        def __str__( self ):
            return "Unable to find declaration.  matcher: [%s]"%str(self.matcher)

    class multiple_declarations_found_t( RuntimeError ):
        def __init__( self, matcher ):
            RuntimeError.__init__( self )
            self.matcher = matcher
            
        def __str__( self ):
            return "Multiple declarations has been found. matcher: [%s]"%str(self.matcher)

    def find( decl_matcher, decls, recursive=True ):
        where = []
        if isinstance( decls, types.ListType ):
            where.extend( decls )
        else:
            where.append( decls )
        if recursive:
            where = algorithm.make_flatten( where )
        return filter( decl_matcher, where )
    find = staticmethod( find )
    
    def find_single( decl_matcher, decls, recursive=True ):
        answer = matcher.find( decl_matcher, decls, recursive )
        if len(answer) == 1:
            return answer[0]
    find_single = staticmethod( find_single )
    
    def get_single( decl_matcher, decls, recursive=True ):
        answer = matcher.find( decl_matcher, decls, recursive )
        if len(answer) == 1:
            return answer[0]
        elif len(answer) == 0:
            raise matcher.declaration_not_found_t( decl_matcher )
        else:
            raise matcher.multiple_declarations_found_t( decl_matcher )
    get_single = staticmethod( get_single )