#!/usr/bin/python

import os
import string
import shutil

def best (filelist):
	bestfile = ""
	bestscore = -1000000.0
	for file in filelist:
		props = string.split(file, "_")
		if len(props)>2:
			try: score = float(props[3])
			except: score = -10000000000
			if score < 0.0 and score > bestscore:
				bestfile = file
				bestscore = score
	return bestfile
	
for dirname in os.listdir('.'):
	if os.path.isdir(dirname) and dirname != "results":

		files = os.listdir(dirname)
		bestfile = best(files)
		print "best file in "+dirname+" is "+bestfile
		if "" != bestfile:
			shutil.copyfile (dirname+"/"+bestfile, "./results/"+bestfile)
		
		
