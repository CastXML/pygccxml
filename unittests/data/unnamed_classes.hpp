// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

#ifndef __unnamed_classes_hpp__
#define __unnamed_classes_hpp__

namespace unnamed{

struct S1{
	struct S2{
		union Flags{
			struct{
				unsigned int hasItemIdList : 1;
				unsigned int pointsToFileOrDir : 1;
				unsigned int hasDescription : 1;
				unsigned int hasRelativePath : 1;
				unsigned int hasWorkingDir : 1;
				unsigned int hasCmdLineArgs : 1;
				unsigned int hasCustomIcon : 1;
				unsigned int useWorkingDir : 1;		// Seems to need to be set to enable working dir
				unsigned int unused : 24;
			};
			unsigned int raw;
		} flags;

		union {
			struct{
				unsigned int isReadOnly : 1;
				unsigned int isHidden : 1;
				unsigned int isSystem : 1;
				unsigned int isVolumeLabel : 1;
				unsigned int isDir : 1;
				unsigned int isModified : 1;	// =archive bit set, ie; is a file normally
				unsigned int isEncrypted : 1;
				unsigned int isNormal : 1;	// Doesn't seem to get set
				unsigned int isTemporary : 1;
				unsigned int isSparse : 1;
				unsigned int hasReparsePoint : 1;
				unsigned int isCompressed : 1;
				unsigned int isOffline : 1;
				unsigned int unused : 19;
			};
			unsigned int raw;
		} fileattribs;		// in GetFileAttributes() format
	} header;

	struct S3{
		union
		{
			char anon_mem_c;
			int anon_mem_i;
		};
		long s3_mem;
		S2 s2;
	};
};

} // namespace
#endif//__unnamed_classes_hpp__
