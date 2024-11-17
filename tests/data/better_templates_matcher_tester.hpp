// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

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
