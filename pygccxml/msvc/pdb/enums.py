from ... import utils #import utils from pygccxml package

class BasicType(utils.enum):
    btNoType   = 0
    btVoid     = 1
    btChar     = 2
    btWChar    = 3
    btInt      = 6
    btUInt     = 7
    btFloat    = 8
    btBCD      = 9
    btBool     = 1
    btLong     = 1
    btULong    = 1
    btCurrency = 2
    btDate     = 2
    btVariant  = 2
    btComplex  = 2
    btBit      = 2
    btBSTR     = 3
    btHresult  = 31



#Adding code, that was not generated for some reason.
class UdtKind(utils.enum):
   UdtStruct, UdtClass, UdtUnion = (0, 1, 2)

class CV_access_e(utils.enum):
   CV_private, CV_protected, CV_public = (1, 2, 3)

class NameSearchOptions(utils.enum):
   nsNone               = 0
   nsfCaseSensitive     = 0x1
   nsfCaseInsensitive   = 0x2
   nsfFNameExt          = 0x4
   nsfRegularExpression = 0x8
   nsfUndecoratedName   = 0x10

   # For backward compabibility:
   nsCaseSensitive           = nsfCaseSensitive
   nsCaseInsensitive         = nsfCaseInsensitive
   nsFNameExt = nsfFNameExt
   nsRegularExpression       = nsfRegularExpression | nsfCaseSensitive
   nsCaseInRegularExpression = nsfRegularExpression | nsfCaseInsensitive

