#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 
# www.genesilico.pl 
#
from Modules.Trans.Interaction 		        import *

from collections					        import OrderedDict

from Modules.Simul.cpp				        import pyry3d_cpp


def flatten_tree(elements, begin=0):
	for el in elements:
		if isinstance(el, SymmetryRestraint):
			send_symmetry(el)
			begin+=1
		elif isinstance(el, ResidueDistanceInteraction):
			send_sd(el)
			begin+=1
		elif isinstance(el, RelationDistances):
			send_relation(el)
			begin+=1
		elif isinstance(el, SurfaceAccessInteraction):
			send_sa(el)
			begin+=1
		elif isinstance(el, PointDistanceInteraction):
			send_pd(el)
			begin+=1
		elif isinstance(el, LogicalRestraint):
			end = flatten_tree(el.elements, begin)
			send_logical(begin, end, el)
			begin = end
	return begin


def get_args_from_pdbranges(a, b, c, d):
	#see filtrest3D for details of classes
	loc = OrderedDict(sorted(locals().items()))
	r_list = []
	for a, i in loc.iteritems():
		r_list.append(i.chain_id)
		if isinstance(i, PDBrange):
			r_list.append(i.res1_num)
			r_list.append(i.res2_num)
		elif isinstance(i, PDBId):
			r_list.append(i.res_num)
			r_list.append(i.res_num)
		
	return r_list

def send_logical(begin, end, inter):
	pyry3d_cpp.add_logical(begin, end, isinstance(inter, AndRestraint))

def send_pd(inter):
	a = inter.restraint.reslist1[0]
	c = inter.restraint
	if not isinstance(a, PDBrange):
		pyry3d_cpp.add_point_distance(a.chain_id, a.res_num, a.res_num, \
			c.dist, c.relation, c.weight, c.point, inter.first_atom_name)
	else:
		pyry3d_cpp.add_point_distance(a.chain_id, a.res1_num, a.res2_num, \
			c.dist, c.relation, c.weight, c.point, inter.first.atom_name)

def send_relation(inter):
	args = get_args_from_pdbranges( inter.restraint.reslist1[0], \
			inter.restraint.reslist2[0], inter.restraint.reslist3[0], \
			inter.restraint.reslist4[0])
	pyry3d_cpp.add_relation_interaction(args[0], args[3], args[6], args[9], \
			args[1], args[2], args[4], args[5], args[7], args[8], args[10], \
			args[11], inter.restraint.relation, inter.first.atom_name, \
			inter.second.atom_name, inter.third.atom_name, inter.fourth.atom_name)

def send_sa(inter):
	a = inter.restraint.reslist1[0]
	c = inter.restraint
	if not isinstance(a, PDBrange):
		pyry3d_cpp.add_surface_access(a.chain_id, a.res_num, a.res_num, \
			c.dist, c.relation, c.weight, inter.first.atom_name)
	else:
		pyry3d_cpp.add_surface_access(a.chain_id, a.res1_num, a.res2_num, \
			c.dist, c.relation, c.weight, inter.first.atom_name)

def send_sd(inter):
	a = inter.restraint.reslist1[0]
	b = inter.restraint.reslist2[0] 
	c = inter.restraint
	if not isinstance(a, PDBrange) and not \
			isinstance(b, PDBrange):
		pyry3d_cpp.add_residue_distance(a.chain_id, b.chain_id, a.res_num, a.res_num, \
			b.res_num, b.res_num, c.dist, c.relation, c.weight, inter.first.atom_name, \
			inter.second.atom_name)
	elif not isinstance(a, PDBrange):
		pyry3d_cpp.add_residue_distance(a.chain_id, b.chain_id, a.res_num, a.res_num, \
			b.res1_num, b.res2_num, c.dist, c.relation, c.weight, inter.first.atom_name, \
			inter.second.atom_name)
	elif not isinstance(b, PDBrange):
		pyry3d_cpp.add_residue_distance(a.chain_id, b.chain_id, a.res1_num, a.res2_num, \
			b.res_num, b.res_num, c.dist, c.relation, c.weight, inter.first.atom_name, \
			inter.second.atom_name)
	else:
		pyry3d_cpp.add_residue_distance(a.chain_id, b.chain_id, a.res1_num, a.res2_num, \
			b.res1_num, b.res2_num, c.dist, c.relation, c.weight, inter.first.atom_name, \
			inter.second.atom_name)	


def send_symmetry(inter):
	distances = []
	for distance in inter.distances:
		a = distance.first
		b = distance.second
		a = pyry3d_cpp.ResidueRange(a.chain_id, a.res1_num, a.res2_num, a.atom_name)
		b = pyry3d_cpp.ResidueRange(b.chain_id, b.res1_num, b.res2_num, b.atom_name)
		distance = pyry3d_cpp.Distance(a, b)
		distances.append(distance)
	pyry3d_cpp.add_symmetry(pyry3d_cpp.DistanceVector(distances))
