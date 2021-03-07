from os import listdir
from os import system
from os.path import isfile, join
import glob
import subprocess
import sys

path = "psweep/config/"
# configfiles = [f for f in listdir(path) if isfile(join(path, f)) and f ]
configfiles = glob.glob(path + sys.argv[1] + '_*')

n = len(configfiles)
nthreads = 1
n_per_batch = int((n + 499) / 500)

print(nthreads, n_per_batch, n)

for i in range(0, n, n_per_batch):
    cmd = "sbatch --job-name=HH_" + sys.argv[1] + " myJobIndividual.sh "
    cmd += " " + str(i)
    cmd += " " + str(n_per_batch + i)
    cmd += " " + sys.argv[1]
    print("CALLING " + cmd)
    system(cmd)
