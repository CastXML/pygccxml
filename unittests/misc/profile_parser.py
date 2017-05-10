# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
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
