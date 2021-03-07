from os import listdir
from os import system
from os.path import isfile, join
import glob
import subprocess
import sys

path = "psweep/config/"
configfiles = glob.glob(path + sys.argv[1] + '_*')

n = len(configfiles)

for i in range(0, n):
    cmd = "sbatch --job-name=HH_" + sys.argv[1] + " myJobIndividual.sh "
    cmd += " " + str(i)
    cmd += " " + str(i)
    cmd += " " + sys.argv[1]
    print("CALLING " + cmd)
    system(cmd)
