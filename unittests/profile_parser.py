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

import os
import hotshot
import hotshot.stats

import autoconfig
import test_parser

if __name__ == "__main__":
    statistics_file = os.path.join(autoconfig.data_directory, 'profile.stat')
    profile = hotshot.Profile(statistics_file)
    profile.runcall(test_parser.run_suite)
    profile.close()
    statistics = hotshot.stats.load(statistics_file)
    statistics.strip_dirs()
    statistics.sort_stats('time', 'calls')
    statistics.print_stats(20)
