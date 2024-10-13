#include "mydll.h"
#include <iostream>

number_t::number_t()
: m_value(0)
{
//	std::cout << "{C++} number_t( 0 )" << std::endl;
}


number_t::number_t(int value)
: m_value(value)
{
//	std::cout << "{C++} number_t( " << value << " )" << std::endl;
}

number_t::~number_t() {
//	std::cout << "{C++} ~number_t()" << std::endl;
}
void number_t::print_it() const {
	std::cout << "{C++} value: " << m_value << std::endl;
}

int number_t::get_value() const{
	return m_value;
}

void number_t::set_value(int x){
	m_value = x;
}

number_t number_t::clone() const{
	return number_t(*this);
}

std::auto_ptr<number_t> number_t::clone_ptr() const{
	return std::auto_ptr<number_t>( new number_t( *this ) );
}

void do_smth( number_aptr_t& ){
}


int myclass_t::my_static_member = 99;
const int myclass_t::my_const_static_member = 10009;
int my_global_int = 90;
volatile int my_volatile_global_variable = 9;
int my_global_array[10] = {0,1,2,3,4,5,6,7,8,9};

void* get_pvoid(void*){ return 0;}
void** get_ppvoid(void){return 0;}

int FA10_i_i(int a[10]){ return 0;}
int FPi_i(int *a){ return 0;}
int Fc_i(char bar){ return 0;}
int Ff_i(float bar){ return 0;}
int Fg_i(double bar){ return 0;}
int Fi_i(int bar){ return 0;}
int Fie_i(int bar, ...){ return 0;}
int Fii_i(int bar, int goo){ return 0;}
int Fiii_i(int bar, int goo, int hoo){ return 0;}
void Fmxmx_v(myclass_t arg1, X arg2, myclass_t arg3, X arg4){}
void Fmyclass_v(myclass_t m){}

const int Fv_Ci(void){ return 0;}
long double Fv_Lg(void){ return 0.0;}
int& Fv_Ri(void){ return my_global_int;}
signed char Fv_Sc(void){ return 0;}
unsigned char Fv_Uc(void){ return 0;}
unsigned int Fv_Ui(void){ return 0;}
unsigned long Fv_Ul(void){ return 0;}
unsigned short Fv_Us(void){ return 0;}
volatile int Fv_Vi(void){ return 0;}
char Fv_c(void){ return 0;}
float Fv_f(void){ return 0.0;}
double Fv_g(void){ return 0.0;}
int Fv_i(void){ return 0;}
long Fv_l(void){ return 0;}
short Fv_s(void){ return 0;}
void Fv_v(void){ return;}

int identity( int i){
    return i;
}

/*
void __cdecl Fv_v_cdecl(void)
void __fastcall Fv_v_fastcall(void)
void __stdcall Fv_v_stdcall(void)
int Fx_i(x fnptr)
int Fxix_i(x fnptr, int i, x fnptr3)
int Fxx_i(x fnptr, x fnptr2)
int Fxxi_i(x fnptr, x fnptr2, x fnptr3, int i)
int Fxxx_i(x fnptr, x fnptr2, x fnptr3)
int Fxyxy_i(x fnptr, y fnptr2, x fnptr3, y fnptr4)
void __cdecl myclass::Fv_v_cdecl(void)
void __fastcall myclass::Fv_v_fastcall(void)
void __stdcall myclass::Fv_v_stdcall(void)
void* myclass::operator new(size_t size)
*/
