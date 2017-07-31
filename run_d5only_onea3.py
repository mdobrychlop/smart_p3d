#!/usr/bin/python

import os, subprocess, sys, math
from multiprocessing import Pool
from itertools import product
import multiprocessing


__author__ = "Lukasz Pawel Kozlowski"
__email__ = "lukaskoz@genesilico.pl"

def runner(command):
    '''popraw polecenie'''
    print "--",command
    os.system(command)
    
def generate_ids(start, end, command):
	'''wygeneruj jakas liste ID'''
	numbers = range(int(start), int(stop), 1)
        print numbers
	commands = []
	for x in numbers:
		commands.append('python pyry3d.py'+command+str(x))
	return commands

if __name__ == '__main__': 
    print '==============================================================================================\n'
    print 'bla bla bla'
    print '==============================================================================================\n'
    
    #get information about number of cpus in your system
    cpu = multiprocessing.cpu_count()
    #adjust cpu number according current load in your machine
    if cpu>1:
        system_load = int(math.ceil(os.getloadavg()[2]))+1
        cpu = cpu-system_load
        if cpu<1: cpu = 1
    
    print cpu, ' CPUs will be used'
    start = sys.argv[1]
    stop = sys.argv[2]
    command = "  --fast -m acc/one_alpha_all_beta.mrc -d acc/onealpha_d5.tar -c acc/config_file_vars_d5only_onealpha.txt -r acc/restraints_D5_only_singleAlpha.txt -s acc/sequences_d5only_onea3.txt -o acc_d5only_onea3/acc_d5only_onea3"
    
    id_list = generate_ids(start, stop, command)
   

    pool = Pool(processes=cpu)               # start N worker processes on N CPUs
    pool.map(runner, id_list) # print out 

    
    
