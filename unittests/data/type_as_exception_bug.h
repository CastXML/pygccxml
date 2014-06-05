#ifndef __key_error_bug_h__
#define __key_error_bug_h__

struct ExpressionError{};
    
struct xxx{
    virtual void buggy() throw( ExpressionError& );
};

#endif//__key_error_bug_h__
