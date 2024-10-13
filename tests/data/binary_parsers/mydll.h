#pragma once

#include "libconfig.h"

#include <memory>
#include <string>
#include <vector>

class EXPORT_SYMBOL number_t{
public:
	number_t();
	explicit number_t(int value);
	virtual ~number_t();
	void print_it() const;
	int get_value() const;
	int get_value(){ return m_value; }
	void set_value(int x);

	number_t clone() const;
	std::auto_ptr<number_t> clone_ptr() const;
private:
	int m_value;
};

template class EXPORT_SYMBOL std::auto_ptr< number_t >;

typedef std::auto_ptr< number_t > number_aptr_t;

enum{ auto_ptr_size = sizeof( number_aptr_t ) };

EXPORT_SYMBOL void do_smth( number_aptr_t& );

EXPORT_SYMBOL extern int my_global_int;

typedef void(*do_smth_type)( number_aptr_t& );

EXPORT_SYMBOL extern volatile int my_volatile_global_variable;

EXPORT_SYMBOL extern int my_global_array[10];

EXPORT_SYMBOL void* get_pvoid(void*);
EXPORT_SYMBOL void** get_ppvoid(void);


class EXPORT_SYMBOL myclass_t{
public:
	myclass_t(int x){}
	myclass_t(void){}
	virtual ~myclass_t(){}
    static int my_static_member;
    static const int my_const_static_member;
    volatile int my_volatile_member;
    
    do_smth_type* get_do_smth(){ return 0; }
    void set_do_smth(do_smth_type*){};
	
	int Fi_i(int bar){ return 0; }
	static int Fis_i(int bar){ return 0; }

	myclass_t operator+(int x){ return myclass_t(); }
	myclass_t operator++(){ return myclass_t(); }
	myclass_t operator++(int){ return myclass_t(); }
	myclass_t& operator=(const myclass_t& from){ return *this;}
	
	struct nested{
		nested(){}
		~nested(){}
		int Fi_i(int bar){ return 0;}
	};

	typedef std::vector< std::wstring > wstring_collection_t;

	wstring_collection_t create_wstring_collection(){ return wstring_collection_t(); }
	void fill_wstring_collection( wstring_collection_t& ){};
	void print__wstring_collection( const wstring_collection_t& ){}


};

struct EXPORT_SYMBOL X{};

EXPORT_SYMBOL int FA10_i_i(int a[10]);
EXPORT_SYMBOL int FPi_i(int *a);
EXPORT_SYMBOL int Fc_i(char bar);
EXPORT_SYMBOL int Ff_i(float bar);
EXPORT_SYMBOL int Fg_i(double bar);
EXPORT_SYMBOL int Fi_i(int bar);
EXPORT_SYMBOL int Fie_i(int bar, ...);
EXPORT_SYMBOL int Fii_i(int bar, int goo);
EXPORT_SYMBOL int Fiii_i(int bar, int goo, int hoo);
EXPORT_SYMBOL void Fmxmx_v(myclass_t arg1, X arg2, myclass_t arg3, X arg4);
EXPORT_SYMBOL void Fmyclass_v(myclass_t m);
EXPORT_SYMBOL const int Fv_Ci(void);
EXPORT_SYMBOL long double Fv_Lg(void);
EXPORT_SYMBOL int& Fv_Ri(void);
EXPORT_SYMBOL signed char Fv_Sc(void);
EXPORT_SYMBOL unsigned char Fv_Uc(void);
EXPORT_SYMBOL unsigned int Fv_Ui(void);
EXPORT_SYMBOL unsigned long Fv_Ul(void);
EXPORT_SYMBOL unsigned short Fv_Us(void);
EXPORT_SYMBOL volatile int Fv_Vi(void);
EXPORT_SYMBOL char Fv_c(void);
EXPORT_SYMBOL float Fv_f(void);
EXPORT_SYMBOL double Fv_g(void);
EXPORT_SYMBOL int Fv_i(void);
EXPORT_SYMBOL long Fv_l(void);
EXPORT_SYMBOL short Fv_s(void);
EXPORT_SYMBOL void Fv_v(void);

extern "C"{
    int EXPORT_SYMBOL identity( int );
}
