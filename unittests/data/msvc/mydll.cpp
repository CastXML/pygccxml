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

