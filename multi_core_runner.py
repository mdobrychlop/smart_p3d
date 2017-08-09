#!/usr/bin/python

import os
import sys
import math
from multiprocessing import Pool
import multiprocessing


__authors__ = "Lukasz Pawel Kozlowski, Mateusz Dobrychlop"
__email__ = "mdobrychlop@genesilico.pl"


def runner(command):
    '''run the command'''
    print "--", command
    os.system(command)


def generate_ids(start, end, command):
    '''generate a list of IDs for jobs'''
    numbers = range(int(start), int(stop), 1)
    print numbers
    commands = []
    for x in numbers:
        commands.append('python pyry3d.py'+command+str(x))
    return commands

if __name__ == '__main__':

    # get information about number of cpus in your system
    cpu = multiprocessing.cpu_count()
    # adjust cpu number according current load in your machine
    if cpu > 1:
        system_load = int(math.ceil(os.getloadavg()[2]))+1
        cpu = cpu-system_load
        if cpu < 1:
            cpu = 1

    print cpu, ' CPUs will be used'
    start = sys.argv[1]
    stop = sys.argv[2]
    command = "  --fast -m map.mrc -d input.tar -c config.txt -r restraints.txt -s sequences.txt -o output"

    id_list = generate_ids(start, stop, command)

    pool = Pool(processes=cpu)  # start N worker processes on N CPUs
    pool.map(runner, id_list)  # print out
