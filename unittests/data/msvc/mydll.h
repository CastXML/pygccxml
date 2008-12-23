#pragma once

#include <memory>
#include <string>
#include <vector>

class __declspec(dllexport) number_t{
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

template class __declspec(dllexport) std::auto_ptr< number_t >;

typedef std::auto_ptr< number_t > number_aptr_t;

enum{ auto_ptr_size = sizeof( number_aptr_t ) };

__declspec(dllexport) void do_smth( number_aptr_t& );

__declspec(dllexport) extern int my_global_int;

typedef void(*do_smth_type)( number_aptr_t& );

__declspec(dllexport) extern volatile int my_volatile_global_variable;

__declspec(dllexport) extern int my_global_array[10];

__declspec(dllexport) void* get_pvoid(void*);
__declspec(dllexport) void** get_ppvoid(void);


class __declspec(dllexport) myclass_t{
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

struct __declspec(dllexport) X{};

__declspec(dllexport) int FA10_i_i(int a[10]);
__declspec(dllexport) int FPi_i(int *a);
__declspec(dllexport) int Fc_i(char bar);
__declspec(dllexport) int Ff_i(float bar);
__declspec(dllexport) int Fg_i(double bar);
__declspec(dllexport) int Fi_i(int bar);
__declspec(dllexport) int Fie_i(int bar, ...);
__declspec(dllexport) int Fii_i(int bar, int goo);
__declspec(dllexport) int Fiii_i(int bar, int goo, int hoo);
__declspec(dllexport) void Fmxmx_v(myclass_t arg1, X arg2, myclass_t arg3, X arg4);
__declspec(dllexport) void Fmyclass_v(myclass_t m);
__declspec(dllexport) const int Fv_Ci(void);
__declspec(dllexport) long double Fv_Lg(void);
__declspec(dllexport) int& Fv_Ri(void);
__declspec(dllexport) signed char Fv_Sc(void);
__declspec(dllexport) unsigned char Fv_Uc(void);
__declspec(dllexport) unsigned int Fv_Ui(void);
__declspec(dllexport) unsigned long Fv_Ul(void);
__declspec(dllexport) unsigned short Fv_Us(void);
__declspec(dllexport) volatile int Fv_Vi(void);
__declspec(dllexport) char Fv_c(void);
__declspec(dllexport) float Fv_f(void);
__declspec(dllexport) double Fv_g(void);
__declspec(dllexport) int Fv_i(void);
__declspec(dllexport) long Fv_l(void);
__declspec(dllexport) short Fv_s(void);
__declspec(dllexport) void Fv_v(void);
