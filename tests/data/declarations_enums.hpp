// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

#ifndef __declarations_enums_hpp__
#define __declarations_enums_hpp__

namespace declarations{ namespace enums{

enum ENumbers{ e0, e1, e2, e3, e4, e5, e6, e7, e8, e9 };

class data{
public:
    enum EColor{ red, green, blue, black, white };
private:
    enum EPrivColor{ priv_red, priv_green, priv_blue, priv_black, priv_white };

    void do_smth(EPrivColor x){}
	EColor favorite_color;
};

} }

#endif//__declarations_enums_hpp__

