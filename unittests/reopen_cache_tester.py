# Copyright 2014-2015 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os
import autoconfig
from pygccxml import parser
from pygccxml import utils


def test_re_opening_cache_file():
    """
    Test re-oping cache files.

    This test is run by file_cache_tester.py in a subprocess.

    """

    data = autoconfig.data_directory

    # xml_generator has not been set
    if utils.xml_generator is not "":
        raise Exception

    # Try to reopen an old cache file and check if there is an exception
    # These old files do not know about the xml generator; a RuntimeError
    # should be thrown, asking to regenerate the cache file.
    c_file = os.path.join(data, 'old_cache.cache')
    error = False
    try:
        parser.file_cache_t(c_file)
    except RuntimeError:
        error = True
    if error is False:
        raise Exception

    # This cache file knows about the xml generator, and was generated
    # with CastXML. Loading the cache should set the utils.xml_generator.
    c_file = os.path.join(data, 'new_cache.cache')
    parser.file_cache_t(c_file)
    if "CastXML" not in utils.xml_generator:
        raise Exception


if __name__ == "__main__":
    test_re_opening_cache_file()
