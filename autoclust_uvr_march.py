#python cluster_complexes.py -i GTEMPY_BENCH_LIPIEC/2rec -s ccc -d mapy/2rec.mrc -v 4.0 -m RMSD -t 10 -r ca -x oligo -o 000_Lip2016_2rec_10A_ca

import os

t="50"
os.system("python cluster_complexes_3ok.py -i results_acc_d5only_onea -s pyry3d -m RMSD -t "+t+" -r ca -o acc_d5only_onea_"+t+" --sort 1")
t="60"
os.system("python cluster_complexes_3ok.py -i results_acc_d5only_onea -s pyry3d -m RMSD -t "+t+" -r ca -o acc_d5only_onea_"+t+" --sort 1")
t="70"
os.system("python cluster_complexes_3ok.py -i results_acc_d5only_onea -s pyry3d -m RMSD -t "+t+" -r ca -o acc_d5only_onea_"+t+" --sort 1")
t="80"
os.system("python cluster_complexes_3ok.py -i results_acc_d5only_onea -s pyry3d -m RMSD -t "+t+" -r ca -o acc_d5only_onea_"+t+" --sort 1")
#t="30"
#os.system("python cluster_complexes_3ok.py -i results_acc33a_feb -s pyry3d -m RMSD -t "+t+" -r ca -o acc33a_feb_"+t+" --sort 1")
#t="40"
#os.system("python cluster_complexes_3ok.py -i results_acc33a_feb -s pyry3d -m RMSD -t "+t+" -r ca -o acc33a_feb_"+t+" --sort 1")
#t="6"
#os.system("python cluster_complexes_3ok.py -i results_trans3 -s pyry3d -m RMSD -t "+t+" -r ca -o uvrm_catr3_"+t)
#t="7"
#os.system("python cluster_complexes_3ok.py -i results_trans3 -s pyry3d -m RMSD -t "+t+" -r ca -o uvrm_catr3_"+t)


