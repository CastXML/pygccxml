# Copyright 2004-2013 Roman Yakovenko
# Copyright 2014 Insight Software Consortium
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

"""
The utils package contains tools used internally by pygccxml.

"""

from .utils import is_str
from .utils import native_compiler
from .utils import get_architecture
from .utils import loggers
from .utils import create_temp_file_name
from .utils import remove_file_no_raise
from .utils import normalize_path
