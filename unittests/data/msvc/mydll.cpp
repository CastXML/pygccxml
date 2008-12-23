#include "mydll.h"
#include "windows.h"
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

BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
					 )
{
	switch (ul_reason_for_call)
	{
	case DLL_PROCESS_ATTACH:
	case DLL_THREAD_ATTACH:
	case DLL_THREAD_DETACH:
	case DLL_PROCESS_DETACH:
		break;
	}
	return TRUE;
}


/*
static int myclass::myStaticMember
const int myclass::myconstStaticMember
volatile int myclass::myvolatileStaticMember
x myfnptr;
int myglobal;
volatile int myvolatile;
int myarray[10];
void **Fv_PPv(void)
void *Fv_Pv(void)
int FA10_i_i(int a[10])
int FPi_i(int *a)
int Fc_i(char bar)
int Ff_i(float bar)
int Fg_i(double bar)
int Fi_i(int bar)
int Fie_i(int bar, ...)
int Fii_i(int bar, int goo)
int Fiii_i(int bar, int goo, int hoo)
void Fmxmx_v(myclass arg1, x arg2, myclass arg3, x arg4)
void Fmyclass_v(myclass m)
const int Fv_Ci(void)
long double Fv_Lg(void)
int& Fv_Ri(void)
signed char Fv_Sc(void)
unsigned char Fv_Uc(void)
unsigned int Fv_Ui(void)
unsigned long Fv_Ul(void)
unsigned short Fv_Us(void)
volatile int Fv_Vi(void)
char Fv_c(void)
float Fv_f(void)
double Fv_g(void)
int Fv_i(void)
long Fv_l(void)
short Fv_s(void)
void Fv_v(void)
void __cdecl Fv_v_cdecl(void)
void __fastcall Fv_v_fastcall(void)
void __stdcall Fv_v_stdcall(void)
int Fx_i(x fnptr)
int Fxix_i(x fnptr, int i, x fnptr3)
int Fxx_i(x fnptr, x fnptr2)
int Fxxi_i(x fnptr, x fnptr2, x fnptr3, int i)
int Fxxx_i(x fnptr, x fnptr2, x fnptr3)
int Fxyxy_i(x fnptr, y fnptr2, x fnptr3, y fnptr4)
void myclass::operator delete(void *p)
int myclass::Fi_i(int bar)
static int myclass::Fis_i(int bar)
void __cdecl myclass::Fv_v_cdecl(void)
void __fastcall myclass::Fv_v_fastcall(void)
void __stdcall myclass::Fv_v_stdcall(void)
myclass::myclass(int x)
myclass::myclass(void)
int myclass::nested::Fi_i(int bar)
myclass::nested::nested(void)
myclass::nested::~nested()
myclass myclass::operator+(int x)
myclass myclass::operator++()
myclass myclass::operator++(int)
myclass& myclass::operator=(const myclass& from)
myclass::~myclass()
int nested::Fi_i(int bar)
nested::nested(void)
nested::~nested()
void* myclass::operator new(size_t size)
*/

