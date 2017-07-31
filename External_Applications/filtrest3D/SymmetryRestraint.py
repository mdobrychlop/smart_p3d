# Copyright '2006 Marta Kaczor, Michal J. Gajda, Anastasia Bakulina
# See license.txt

import PModel  #getting access to stride_dict
from Restraint import Restraint
import sys
from PDBId import PDBId

def list_middle_item(l):
  index=len(l)/2
  return l[index]

class Symmetry(Restraint):
    'check distance between two sets (or pair) of residues'
    type=["Distance"]
    
    def __init__(self, distances, id=''):
       self.distances = distances
       #self.dist = distance
       #self.relation = relation
       #self.weight = weight 
       self.id = id
       
    def __str__(self):
      return "%s %s %s %s %s" % \
              (self.reslist1, self.restlist2, self.relation, self.weight, self.id)
            
    def __reslist2str__ (self,reslist):
       str1 = '('
       for res in reslist:
          str1 += str(res)+','
       str1 += ')'   
       return str1

    def short_name(self):
       if self.id!="":
         return self.id
       else:
         return self.name()[1:]

    def autoname(self):
        return ','.join(self.__reslist2str__(d[0])+'-'+self.__reslist2str__(d[1]) for d in self.distances)
