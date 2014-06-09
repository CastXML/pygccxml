/*=========================================================================
 *
 *  Copyright 2014 Insight Software Consortium
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *         http://www.apache.org/licenses/LICENSE-2.0.txt
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 *
 *=========================================================================*/

// Copyright 2004-2013 Roman Yakovenko.
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

