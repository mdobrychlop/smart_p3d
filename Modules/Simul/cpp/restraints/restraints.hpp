#ifndef RESTRAINTS_PYRY3D
#define RESTRAINTS_PYRY3D

using std::string;

enum Relation {
	LT, LE, GE, GT
};

class Restraint {
public:
	virtual ~Restraint() {
	}

	virtual float score(int complex_index) const = 0;

	virtual bool isSymmetry() const {
		return false;
	}
};

class Logical {
	int begin;
	int end;
	bool max;
public:
	Logical(int b, int e, bool isAnd);

	void score(int complex_index) const;
};

struct ResidueRange {
	int chain_index;
	int begin;
	int end;
	string atom_name;

	ResidueRange(const string& chain_name, int begin, int end,
			const string& atom_name);
};

class RelationRestraint: public Restraint {
	Relation relation;
protected:
	float distance;
	float weight;
public:
	RelationRestraint(const string& rel, float dist, float weight);

	virtual float score(int complex_index) const = 0;

	bool update_min_diff(float& min_diff, float new_diff) const;
};

class PointDistance: public RelationRestraint {
	ResidueRange range;
	point p;
public:
	PointDistance(const string& first, int a1, int a2, float dist,
			const string& rel, float weight, const std::vector<float>& point_v,
			const string& f_a_n);

	float score(int complex_index) const;
};

class ResidueDistance: public RelationRestraint {
	ResidueRange first;
	ResidueRange second;
public:
	ResidueDistance(const string& first, const string& second, int a1, int a2,
			int b1, int b2, float dist, const string& rel, float weight,
			const string& f_a_n, const string& s_a_n);

	float score(int complex_index) const;
};

class RelationDistance: public Restraint {
	Relation relation;
	ResidueRange first;
	ResidueRange second;
	ResidueRange third;
	ResidueRange fourth;
public:
	RelationDistance(const string& first, const string& second,
			const string& third, const string& fourth, int a1, int a2, int b1,
			int b2, int c1, int c2, int d1, int d2, const string& rel,
			const string& f_a_n, const string& s_a_n, const string& t_a_n,
			const string& fo_a_n);

	float score(int complex_index) const;
};

class SurfaceAccess: public RelationRestraint {
	ResidueRange range;
public:
	SurfaceAccess(const string& first, int a1, int a2, float dist,
			const string& rel, float weight, const string& f_a_n);

	float score(int complex_index) const;
};

class Distance {
	ResidueRange first;
	ResidueRange second;
public:
	Distance(const ResidueRange& first, const ResidueRange& second);

	float compute(int complex_index) const;
};

class Symmetry: public Restraint {
	std::vector<Distance> distances;
public:
	Symmetry(std::vector<Distance>& distances);

	float score(int complex_index) const;

	bool isSymmetry() const {
		return true;
	}
};

void update_restraints_score(int complex_index);
void calculate_restraints_score(int complex_index);
void calculate_symmetry_score(int complex_index);

#endif
