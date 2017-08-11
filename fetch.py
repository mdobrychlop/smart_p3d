#!/usr/bin/python

import os
import shutil


def determine_pyry3d_score(filename):
    """
    Finds a PyRy3D score substring in a PDB file's name.
    VERY simplified, but works for filenames with score
    located between underscores.

    Example:

    Input: "acc_d5only_onea360_-375.633_195000_0.000115178.pdb"
    Output: -375.633

    """
    pieces = filename.split("_")
    score = 0.0
    for piece in pieces:
        if piece.startswith("-") and "." in piece:
            score = float(piece)
    return score


def best(filelist):
    bestfile = ""
    bestscore = -9999999.0
    for file in filelist:
        score = determine_pyry3d_score(file)
        if score < 0.0 and score > bestscore:
            bestfile = file
            bestscore = score
    return bestfile

if os.path.exists("results") is False:
    os.mkdir("results")

counter = 0
for dirname in os.listdir('.'):
    if os.path.isdir(dirname) and dirname != "results":

        files = os.listdir(dirname)
        bestfile = best(files)
        print "best file in "+dirname+" is "+bestfile
        if "" != bestfile:
            shutil.copyfile(dirname+"/"+bestfile, "./results/"+bestfile)
            counter += 1

print "Models extracted: ", counter
