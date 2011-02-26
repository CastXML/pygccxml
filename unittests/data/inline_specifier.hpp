struct text_t{
	inline bool inlined() const { return true; }
	unsigned long not_inlined() const;
};


inline bool inlined(text_t){ return true; }
unsigned long not_inlined(text_t);
