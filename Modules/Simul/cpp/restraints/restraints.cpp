#include "../extern.hpp"

#include <cassert>

template<class T>
typename std::enable_if<!std::numeric_limits<T>::is_integer, bool>::type almost_equal(
		T x, T y) {
	// the machine epsilon has to be scaled to the magnitude of the values used
	return std::abs(x - y) < std::numeric_limits<T>::epsilon() * std::abs(x + y)
	// unless the result is subnormal
			|| std::abs(x - y) < std::numeric_limits<T>::min();
}

void update_restraints_score(int complex_index) {
	for (size_t i = 0; i < restraints.size(); ++i) {
		complexes[complex_index].res_scores[i] = restraints[i]->score(complex_index);
	}
	for (auto l : logical) {
		l.score(complex_index);
	}
}

void calculate_restraints_score(int complex_index) {
	float score = 0.0f;
	for (size_t i = 0; i < restraints.size(); ++i) {
		if (!restraints[i]->isSymmetry()
				&& complexes[complex_index].res_scores[i] != -1) {
			score += complexes[complex_index].res_scores[i]
					* complexes[complex_index].res_scores[i];
		}
	}
	complexes[complex_index].restraints = -std::sqrt(score);
}

void calculate_symmetry_score(int complex_index) {
	float score = 0.0f;
	for (size_t i = 0; i < restraints.size(); ++i) {
		if (restraints[i]->isSymmetry()
				&& complexes[complex_index].res_scores[i] != -1) {
			score += complexes[complex_index].res_scores[i];
		}
	}
	complexes[complex_index].symmetry = -score;
}

const string& get_chain_name(int index) {
	return chain_identifiers[residue_indexes[chain_indexes[index]]];
}

int get_chain_index(const string& name) {
	for (int i = 0; i < chain_counter; ++i) {
		if (get_chain_name(i) == name) {
			return i;
		}
	}
	throw;
}

int get_atom_index(int chain_index, int residue_index,
		const string& atom_name) {
	int i = residue_to_index[CURR_COMPONENT(chain_index) + residue_index - 1];
	while (atom_names[i] != atom_name)
		++i;
	return i;
}

Relation get_relation_id(const string& s) {
	if (s == "<")
		return LT;
	if (s == "<=")
		return LE;
	if (s == ">=")
		return GE;
	if (s == ">")
		return GT;
	throw;
}

bool RelationRestraint::update_min_diff(float& min_diff, float new_diff) const {
	if ((relation == LT || relation == LE) && new_diff < 0) {
		return true;
	}

	if ((relation == GT || relation == GE) && new_diff > 0) {
		return true;
	}

	if (almost_equal(new_diff, 0.0f)) {
		return true;
	}

	new_diff = std::abs(new_diff);
	if (new_diff < min_diff) {
		min_diff = new_diff;
	}

	return false;
}

ResidueRange::ResidueRange(const string& chain_name, int begin, int end,
		const string& atom_name) :
		chain_index(get_chain_index(chain_name)), begin(begin), end(end + 1), atom_name(
				atom_name) {
}

Logical::Logical(int b, int e, bool isAnd) :
		begin(b), end(e), max(isAnd) {
}

void Logical::score(int complex_index) const {
	/* it throws -1 everywhere where scores should not be inserted into result !!!
	 Error prone*/

	float value;
	int index = -1;

	if (max) {
		value = -1;
		for (int i = begin; i < end; ++i) {
			if (complexes[complex_index].res_scores[i] > value) {
				value = complexes[complex_index].res_scores[i];
				index = i;
			}
		}
	} else {
		value = std::numeric_limits<float>::max();
		for (int i = begin; i < end; ++i) {
			if (complexes[complex_index].res_scores[i] == -1) // ignore removed
				continue;
			if (complexes[complex_index].res_scores[i] < value) {
				value = complexes[complex_index].res_scores[i];
				index = i;
			}
		}
	}

	assert(index != -1);

	// remove unused
	for (int i = begin; i < index; ++i) {
		complexes[complex_index].res_scores[i] = -1;
	}
	for (int i = index + 1; i < end; ++i) {
		complexes[complex_index].res_scores[i] = -1;
	}
}

PointDistance::PointDistance(const string& f, int a1, int a2, float dist,
		const string& rel, float weight, const std::vector<float>& point_v,
		const string& f_a_n) :
		RelationRestraint(rel, dist, weight), range(f, a1, a2, f_a_n), p(
				point_v) {
}

float PointDistance::score(int complex_index) const {
	float min_diff = std::numeric_limits<float>::max();

	for (int i = range.begin; i < range.end; ++i) {
		int i_atom = get_atom_index(range.chain_index, i, range.atom_name);
		float new_diff = dist(complexes[complex_index].coords[i_atom], p)
				- distance;
		if (update_min_diff(min_diff, new_diff)) {
			return 0;
		}
	}

	assert(min_diff < std::numeric_limits<float>::max());

	return weight * min_diff;
}

void get_pair_score(int complex_index, const ResidueRange& first,
		const ResidueRange& second, float& min_dist, float& max_dist) {
	min_dist = std::numeric_limits<float>::max();
	max_dist = -1;

	for (int i = first.begin; i < first.end; ++i) {
		int i_atom = get_atom_index(first.chain_index, i, first.atom_name);
		for (int j = second.begin; j < second.end; ++j) {
			int j_atom = get_atom_index(second.chain_index, j,
					second.atom_name);
			float new_dist = dist(complexes[complex_index].coords[i_atom],
					complexes[complex_index].coords[j_atom]);
			if (new_dist < min_dist)
				min_dist = new_dist;
			if (new_dist > max_dist)
				max_dist = new_dist;
		}
	}

	assert(min_dist < std::numeric_limits<float>::max());
	assert(max_dist >= 0);
}

RelationDistance::RelationDistance(const string& first, const string& second,
		const string& third, const string& fourth, int a1, int a2, int b1,
		int b2, int c1, int c2, int d1, int d2, const string& rel,
		const string& f_a_n, const string& s_a_n, const string& t_a_n,
		const string& fo_a_n) :
		relation(get_relation_id(rel)), first(first, a1, a2, f_a_n), second(
				second, b1, b2, s_a_n), third(third, c1, c2, t_a_n), fourth(
				fourth, d1, d2, fo_a_n) {
}

float RelationDistance::score(int complex_index) const {
	float res[2][2];
	get_pair_score(complex_index, first, second, res[0][0], res[0][1]);
	get_pair_score(complex_index, third, fourth, res[1][0], res[1][1]);
	if (relation == LT || relation == LE)
		return res[0][0] <= res[1][1] ? 0 : 100;
	else
		return res[0][1] >= res[1][0] ? 0 : 100;
}

RelationRestraint::RelationRestraint(const string& rel, float dist,
		float weight) :
		relation(get_relation_id(rel)), distance(dist), weight(weight) {
}

ResidueDistance::ResidueDistance(const string& first, const string& second,
		int a1, int a2, int b1, int b2, float dist, const string& rel,
		float weight, const string& f_a_n, const string& s_a_n) :
		RelationRestraint(rel, dist, weight), first(first, a1, a2, f_a_n), second(
				second, b1, b2, s_a_n) {
}

float ResidueDistance::score(int complex_index) const {
	float min_diff = std::numeric_limits<float>::max();

	for (int i = first.begin; i < first.end; ++i) {
		int i_atom = get_atom_index(first.chain_index, i, first.atom_name);
		for (int j = second.begin; j < second.end; ++j) {
			int j_atom = get_atom_index(second.chain_index, j,
					second.atom_name);
			float new_diff = dist(complexes[complex_index].coords[i_atom],
					complexes[complex_index].coords[j_atom]) - distance;
			if (update_min_diff(min_diff, new_diff)) {
				return 0;
			}
		}
	}

	assert(min_diff < std::numeric_limits<float>::max());

	return weight * min_diff;
}

SurfaceAccess::SurfaceAccess(const string& first, int a1, int a2, float dist,
		const string& rel, float weight, const string& f_a_n) :
		RelationRestraint(rel, dist, weight), range(first, a1, a2, f_a_n) {
}

float SurfaceAccess::score(int complex_index) const {
	float min_diff = std::numeric_limits<float>::max();

	for (int i = range.begin; i < range.end; ++i) {
		int i_atom = get_atom_index(range.chain_index, i, range.atom_name);
		for (size_t j = 0; j < surface.size(); ++j) {
			float new_diff = dist(complexes[complex_index].coords[i_atom],
					surface[j]) - distance;
			if (update_min_diff(min_diff, new_diff)) {
				return 0;
			}
		}
	}

	assert(min_diff < std::numeric_limits<float>::max());

	return weight * min_diff;
}

Distance::Distance(const ResidueRange& first, const ResidueRange& second) :
		first(first), second(second) {
}

float Distance::compute(int complex_index) const {
	float min_dist = std::numeric_limits<float>::max();

	for (int i = first.begin; i < first.end; ++i) {
		int i_atom = get_atom_index(first.chain_index, i, first.atom_name);
		for (int j = second.begin; j < second.end; ++j) {
			int j_atom = get_atom_index(second.chain_index, j,
					second.atom_name);
			float new_dist = dist(complexes[complex_index].coords[i_atom],
					complexes[complex_index].coords[j_atom]);
			if (almost_equal(new_dist, 0.0f)) {
				return 0;
			}
			if (new_dist < min_dist) {
				min_dist = new_dist;
			}
		}
	}

	assert(min_dist < std::numeric_limits<float>::max());

	return min_dist;
}

Symmetry::Symmetry(std::vector<Distance>& distances) :
		distances(distances) {
}

float Symmetry::score(int complex_index) const {
	float product = 1.0f;
	float distanceValues[distances.size()];
	for (size_t i = 0; i < distances.size(); ++i) {
		distanceValues[i] = distances[i].compute(complex_index);
		product *= distanceValues[i];
	}
	float average = std::pow(product, 1.0f / (float) distances.size());
	float score = 0.0f;
	for (size_t i = 0; i < distances.size(); ++i) {
		score += std::abs(distanceValues[i] - average);
	}
	return score;
}
