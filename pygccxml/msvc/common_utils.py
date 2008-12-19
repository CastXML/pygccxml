import ctypes

class UNDECORATE_NAME_OPTIONS:
    UNDNAME_COMPLETE = 0
    UNDNAME_NO_LEADING_UNDERSCORES = 1
    UNDNAME_NO_MS_KEYWORDS = 2
    UNDNAME_NO_FUNCTION_RETURNS = 4
    UNDNAME_NO_ALLOCATION_MODEL = 8
    UNDNAME_NO_ALLOCATION_LANGUAGE = 16
    UNDNAME_NO_MS_THISTYPE = 32
    UNDNAME_NO_CV_THISTYPE = 64
    UNDNAME_NO_THISTYPE = 96
    UNDNAME_NO_ACCESS_SPECIFIERS = 128
    UNDNAME_NO_THROW_SIGNATURES = 256
    UNDNAME_NO_MEMBER_TYPE = 512
    UNDNAME_NO_RETURN_UDT_MODEL = 1024
    UNDNAME_32_BIT_DECODE = 2048
    UNDNAME_NAME_ONLY = 4096
    UNDNAME_NO_ARGUMENTS = 8192
    UNDNAME_NO_SPECIAL_SYMS = 16384

    UNDNAME_SCOPES_ONLY = UNDNAME_NO_LEADING_UNDERSCORES \
                          | UNDNAME_NO_MS_KEYWORDS \
                          | UNDNAME_NO_FUNCTION_RETURNS \
                          | UNDNAME_NO_ALLOCATION_MODEL \
                          | UNDNAME_NO_ALLOCATION_LANGUAGE \
                          | UNDNAME_NO_ACCESS_SPECIFIERS \
                          | UNDNAME_NO_THROW_SIGNATURES \
                          | UNDNAME_NO_MEMBER_TYPE


undecorate_name_impl = ctypes.windll.dbghelp.UnDecorateSymbolName
undecorate_name_impl.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint, ctypes.c_uint]

def undecorate_name( name, options=None ):
    if options is None:
        options = UNDECORATE_NAME_OPTIONS.UNDNAME_COMPLETE
    buffer = ctypes.create_string_buffer(1024*16)
    res = undecorate_name_impl(name, buffer, ctypes.sizeof(buffer), options)
    if res:
        return str(buffer[:res])
    else:
        return name
