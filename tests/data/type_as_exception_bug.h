// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

#ifndef __key_error_bug_h__
#define __key_error_bug_h__

struct ExpressionError{};
    
struct xxx{
    virtual void buggy() throw( ExpressionError& );
};

#endif//__key_error_bug_h__
