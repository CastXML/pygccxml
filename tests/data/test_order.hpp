// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

const int c1 = 0;
int const c2 = 0;

const int * const cptr1 = 0;
int const * const cptr2 = 0;

volatile int v1 = 0;
int volatile v2 = 0;

volatile int * volatile vptr1 = 0;
int volatile * volatile vptr2 = 0;

const volatile int cv1 = 0;
int const volatile cv2 = 0;
volatile const int cv3 = 0;
int volatile const cv4 = 0;

const volatile int * const volatile cvptr1 = 0;
int const volatile * const volatile cvptr2 = 0;
volatile const int * volatile const cvptr3 = 0;
int volatile const * volatile const cvptr4 = 0;

const int ac1[2] = {};
int const ac2[2] = {};

const int * const acptr1[2] = {};
int const * const acptr2[2] = {};

class A {};
const class A classA = {};