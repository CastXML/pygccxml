#Adding code, that was not generated for some reason.
class UdtKind:
   UdtStruct, UdtClass, UdtUnion = (0, 1, 2)

class CV_access_e:
   CV_private, CV_protected, CV_public = (1, 2, 3)

class NameSearchOptions:
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

