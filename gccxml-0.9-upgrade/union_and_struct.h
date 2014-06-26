// Copyright 2014 Insight Software Consortium.
// Copyright 2004-2007 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

struct position{
    union {
        struct {
            float x, y, z;
        };
        float val[3];
    };

    static const position zero;
};
