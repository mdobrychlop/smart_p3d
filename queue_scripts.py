"""
Script for generating a set of slurm-understandable scripts, and then
running the scripts using slurm queue system.
"""
import os
import time


__author__ = "Mateusz Dobrychlop"

CX_NAME = "1gte"
SIM_NUMBER = 350

content = """#!/bin/bash -l
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem=32gb
#SBATCH -p  standard

module load python/2.7.3
module load gcc

source ../bin/activate
"""

results_loc = CX_NAME + "_proper"

mapname = CX_NAME + "/" + CX_NAME + ".mrc "
tarname = CX_NAME + "/" + CX_NAME + ".tar "
cfgname = CX_NAME + "/" + CX_NAME + "_cfg.txt"
outname = results_loc + "/" + CX_NAME + "_mdbench_"

if os.path.exists(results_loc) is False:
    os.mkdir(results_loc)

script_loc_name = CX_NAME + "_scripts"

for i in range(0, SIM_NUMBER+1):
    p3d_line = "python pyry3d.py --fast -c " + cfgname + " -m " + mapname + \
               "-d " + tarname + "-o " + outname + str(i)
    cont = content + p3d_line
    if os.path.exists(script_loc_name) is False:
        os.mkdir(script_loc_name)
    script_file_path = script_loc_name + "/" + CX_NAME + str(i) + ".sl"
    script_file = open(script_file_path, "w")
    script_file.write(cont)
    script_file.close()

    os.system("sbatch "+script_file_path)
    time.sleep(2)
