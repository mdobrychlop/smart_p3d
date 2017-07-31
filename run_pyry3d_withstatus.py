import os
import sys
import math
import multiprocessing

# based on a script by Lukasz Pawel Kozlowski


class SimulationBatch():
    def __init__(self, jobid, indir, simcount):
        self.jobid = jobid
        self.indir = indir
        self.simcount = simcount

    def runner(self, command):
        print "--", command
        os.system(command)

    def generate_ids(self, start, end, command):
        numbers = range(int(start), int(end), 1)
        print numbers
        commands = []
        for x in numbers:
            commands.append('python pyry3d.py'+command+str(x))
        return commands

    def run(self):
        # get information about number of cpus in your system
        cpu = multiprocessing.cpu_count()
        # adjust cpu number according to current load on your machine
        if cpu > 1:
            system_load = int(math.ceil(os.getloadavg()[2]))+1
            cpu = cpu-system_load
            if cpu < 1:
                cpu = 1

        print cpu, ' CPUs will be used'
        start = sys.argv[1]
        stop = sys.argv[2]
        command = "  --fast \
                   -m acc/one_alpha_all_beta.mrc \
                   -d acc/onealpha_d5.tar \
                   -c acc/config_file_vars_d5only_onealpha.txt \
                   -r acc/restraints_D5_only_singleAlpha.txt \
                   -s acc/sequences_d5only_onea3.txt \
                   -o acc_d5only_onea3/acc_d5only_onea3"

        id_list = self.generate_ids(start, stop, command)

        pool = multiprocessing.Pool(processes=cpu)
        pool.map(self.runner, id_list)


if __name__ == "__main__":
    input_dir = sys.argv[1]
    simcount = sys.argv[2]
    job_id = sys.argv[3]

    batch = SimulationBatch(job_id, input_dir, simcount)
    batch.run()
