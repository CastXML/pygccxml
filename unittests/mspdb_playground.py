import os
import unittest
import autoconfig

import pprint
from pygccxml.msvc import mspdb
from pygccxml import declarations
from pygccxml.msvc import common_utils as msvc_utils

pdb_file = r'E:\development\language-binding\pyplusplus_dev\pyplusplus\cpptypes\mydll\release\mydll.pdb'

reader = mspdb.decl_loader_t( pdb_file )
opt = mspdb.enums.UNDECORATE_NAME_OPTIONS.UNDNAME_SHORT_UNIQUE

d = {}
for smbl in reader.public_symbols.itervalues():
    name = smbl.name
    undecorated_name = smbl.get_undecoratedNameEx(opt).strip()
    if undecorated_name.endswith( ')const' ):
        undecorated_name = undecorated_name[ : -len('const')]
    d[ name ] = undecorated_name
    d[ undecorated_name ] = name

pprint.pprint( d )

#~ reader.read()
#~ f = file( 'decls.cpp', 'w+' )
#~ declarations.print_declarations( reader.global_ns, writer=lambda line: f.write(line+'\n') )
#~ f.close()

#~ f = file( 'symbols.txt', 'w+')
#~ for smbl in reader.symbols.itervalues():
    #~ f.write( smbl.uname )
    #~ f.write( os.linesep )
    #~ f.write( '\t' + str(smbl.name) )
#~ f.close()

