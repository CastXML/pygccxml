# Copyright 2004-2013 Roman Yakovenko
# Copyright 2014 Insight Software Consortium
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

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
