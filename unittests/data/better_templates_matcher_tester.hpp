// Copyright 2004-2013 Roman Yakovenko
// Copyright 2014 Insight Software Consortium
// Distributed under the Boost Software License, Version 1.0.
// (See accompanying file LICENSE.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#include <vector>
#include <map>

namespace Ogre{
    struct PlaneBoundedVolume{};

    struct Plane{};

    std::vector<PlaneBoundedVolume> do_smth(){
        return std::vector<PlaneBoundedVolume>();
    }

    std::vector<Plane> do_smth2(){
        return std::vector<Plane>();
    }

    template< class X >
    struct Singleton{
    };

    struct PCZoneFactoryManager{};

    Singleton<PCZoneFactoryManager> do_smth3(){
        return Singleton<PCZoneFactoryManager>();
    }
}
