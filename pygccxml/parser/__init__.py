# =============================================================================
#
#  Copyright 2014 Insight Software Consortium
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0.txt
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# =============================================================================

# Copyright 2004-2013 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

"""Parser sub-package.
"""

from .config import gccxml_configuration_t
from .config import load_gccxml_configuration
from .config import gccxml_configuration_example

from .project_reader import COMPILATION_MODE
from .project_reader import project_reader_t
from .project_reader import file_configuration_t
from .project_reader import create_text_fc
from .project_reader import create_source_fc
from .project_reader import create_gccxml_fc
from .project_reader import create_cached_source_fc

from .source_reader import source_reader_t
from .source_reader import gccxml_runtime_error_t
from .declarations_cache import cache_base_t
from .declarations_cache import file_cache_t
from .declarations_cache import dummy_cache_t
from .directory_cache import directory_cache_t
# shortcut
CONTENT_TYPE = file_configuration_t.CONTENT_TYPE


def parse(
        files,
        config=None,
        compilation_mode=COMPILATION_MODE.FILE_BY_FILE,
        cache=None):
    """
    Parse header files.

    :param files: The header files that should be parsed
    :type files: list of str
    :param config: Configuration object or None
    :type config: :class:`parser.gccxml_configuration_t`
    :param compilation_mode: Determines whether the files are parsed
                             individually or as one single chunk
    :type compilation_mode: :class:`parser.COMPILATION_MODE`
    :param cache: Declaration cache (None=no cache)
    :type cache: :class:`parser.cache_base_t` or str
    :rtype: list of :class:`declarations.declaration_t`
    """
    if not config:
        config = gccxml_configuration_t()
    parser = project_reader_t(config=config, cache=cache)
    answer = parser.read_files(files, compilation_mode)
    return answer


def parse_string(content, config=None):
    if not config:
        config = gccxml_configuration_t()
    parser = project_reader_t(config)
    return parser.read_string(content)


def parse_xml_file(content, config=None):
    parser = source_reader_t(config)
    return parser.read_xml_file(content)
