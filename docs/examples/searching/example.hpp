// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

namespace ns{
    int a = 1;
    int b = 2;
    double c = 3.0;

    int func1(int a) {
        int b = a + 2;
        return b;
    }

    double func2(double a) {
        double b = a + 2.0;
        return b;
    }

     double func3(double a) {
        double b = a + 3.0;
        return b;
    }
}
