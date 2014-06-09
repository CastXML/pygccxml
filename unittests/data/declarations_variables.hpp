/*=========================================================================
 *
 *  Copyright Insight Software Consortium
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

// Copyright 2004-2008 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

#ifndef __declarations_variables_hpp__
#define __declarations_variables_hpp__

namespace declarations{ namespace variables{

const long unsigned int initialized = 10122004;
int array[255];

//TODO: explain why such variables is not peeked
extern int static_var;

struct struct_variables_t{
    mutable int m_mutable;
};

struct struct_variables_holder_t{
	struct_variables_t m_struct_variables;
};

} }

#endif//__declarations_variables_hpp__

