#include <string>
#include "abstract_classes.hpp"
#include "attributes.hpp"
#include "bit_fields.hpp"
#include "complex_types.hpp"
#include "core_cache.hpp"
#include "core_types.hpp"
#include "core_class_hierarchy.hpp"
#include "core_diamand_hierarchy_base.hpp"
#include "core_diamand_hierarchy_derived1.hpp"
#include "core_diamand_hierarchy_derived2.hpp"
#include "core_diamand_hierarchy_final_derived.hpp"
#include "core_membership.hpp"
#include "core_ns_join_1.hpp"
#include "core_ns_join_2.hpp"
#include "core_ns_join_3.hpp"
#include "core_overloads_1.hpp"
#include "core_overloads_2.hpp"
#include "core_types.hpp"
#include "declarations_calldef.hpp"
#include "declarations_comparison.hpp"
#include "declarations_enums.hpp"
#include "declarations_for_filtering.hpp"
#include "declarations_variables.hpp"
#include "demangled.hpp"
#include "free_operators.hpp"
#include "has_public_binary_operator_traits.hpp"
#include "include_all.hpp"
#include "include_std.hpp"
#include "indexing_suites2.hpp"
#include "noncopyable.hpp"
#include "patcher.hpp"
#include "remove_template_defaults.hpp"
#include "string_traits.hpp"
#include "type_as_exception_bug.h"
#include "type_traits.hpp"
#include "typedefs1.hpp"
#include "typedefs2.hpp"
#include "typedefs_base.hpp"
#include "unnamed_classes.hpp"
#include "unnamed_enums_bug1.hpp"
#include "unnamed_enums_bug2.hpp"
#include "unnamed_ns_bug.hpp"
#include "vector_traits.hpp"
#include "core_types.hpp"


namespace core{ namespace overloads{

void do_nothing( std::string d){ std::cout << d; }
void do_nothing( std::wstring d){ std::wcout << d; }
void do_nothing( std::set< std::string > d ){ std::set< std::string >::size_type t = d.size(); }
void do_nothing( std::set< std::wstring > d ){ std::set< std::wstring >::size_type t = d.size(); }

} }

namespace declarations{ namespace variables{

int static_var = 0;
}}

void use_decls(){	
	declarations::enums::ENumbers enumbers;
	declarations::enums::data::EColor ecolor;

	sizeof(core::types::exception );
}

void use_core_overloads(){
	namespace co = core::overloads;
}

void use_core_types(){
	use_core_overloads();
	core::types::members_pointers_t mem_ptrs;
	core::types::typedef_const_int typedef_const_int_ = 0;
	core::types::typedef_pointer_int typedef_pointer_int_ = 0;
	int i = 0;
	core::types::typedef_reference_int typedef_reference_int_ = i;
	unsigned int j = 0;
	core::types::typedef_const_unsigned_int_const_pointer typedef_const_unsigned_int_const_pointer_ = &j;
	core::types::typedef_void* typedef_void = 0;
	core::types::typedef_char typedef_char_;
	core::types::typedef_signed_char typedef_signed_char_;
	core::types::typedef_unsigned_char typedef_unsigned_char_;
	core::types::typedef_wchar_t typedef_wchar_t_;
	core::types::typedef_short_int typedef_short_int_;
	core::types::typedef_signed_short_int typedef_signed_short_int_;
	core::types::typedef_short_unsigned_int typedef_short_unsigned_int_;
	core::types::typedef_bool typedef_bool_;
	core::types::typedef_int typedef_int_;
	core::types::typedef_signed_int typedef_signed_int_;    
	core::types::typedef_unsigned_int typedef_unsigned_int_;
	core::types::typedef_long_int typedef_long_int_;
	core::types::typedef_long_unsigned_int typedef_long_unsigned_int_;
	core::types::typedef_long_long_int typedef_long_long_int_;
	core::types::typedef_long_long_unsigned_int typedef_long_long_unsigned_int_;
	core::types::typedef_float typedef_float_;
	core::types::typedef_double typedef_double_;
	core::types::typedef_long_double typedef_long_double_;
	core::types::typedef_volatile_int typedef_volatile_int_;
	core::types::member_variable_ptr_t member_variable_ptr_ = 0;
	core::types::typedef_EFavoriteDrinks typedef_EFavoriteDrinks_;

	std::wstring hello_world;

	core::types::function_ptr function_ptr_ = 0;
	core::types::member_function_ptr_t member_function_ptr_ = 0;

	core::types::members_pointers_t members_pointers_inst;
	members_pointers_inst.some_function( 0.23 );
	members_pointers_inst.some_function( 0.23, 11 );

}

void use_core_ns_join_3(){
	E31 e31_;
	ns::E32 e32_;
	ns::ns32::E33 e33_;
	ns::E34 e34_;


	 E11 e11_;
	 E21 e21_;
	 ns::E12 e12_;
	 ns::E22 e22_;
	 ns::ns12::E13 e13_;
	 ns::ns22::E23 e23_;
}

void use_coremembership(){
	namespace cm = core::membership;
	int i = cm::enums_ns::WITHIN_NS_UNNAMED_ENUM;
	i += cm::enums_ns::WITHIN_NS;
	i += cm::WITHIN_UNNAMED_NS_UNNAMED_ENUM;
	i += cm::WITHIN_UNNAMED_NS;
	cm::class_for_nested_enums_t class_for_nested_enums_; 

	i += ::GLOBAL_NS_UNNAMED_ENUM;
	EGlobal eglobal_;
	
}
