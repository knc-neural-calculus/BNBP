from os import listdir
from os.path import isdir, join
import os
import sys
import math
import glob

import numpy as np
import pandas as pd
from typing import *

def fcomp(a,b,delta = 1e-5):
	return abs(a-b) < delta

from psweep import *



def read_loss(
		filename,
		mode = 'abs',
		first_n = 5,
		last_n = 5,
	):
		
	try:
		data = np.genfromtxt(filename, delimiter=',')
	except ValueError:
		return float('nan')

	try:
		data = data[:,:-1]
	except:
		return float('nan')
	
	avg_final_loss = np.average(data[-last_n:])

	if mode == 'abs':
		return avg_final_loss
	elif mode == 'rel':
		# loss_first = np.average(np.amin(np.average(data[:first_n], axis = 1)))
		loss_first = np.average(data[:first_n])
		return avg_final_loss / loss_first


def read_percent(filename) -> float:
	try:
		pair = open(filename, "r").readlines()[-1]
		return float(pair.split('\t')[-1])
		# tab_idx = pair.find('\t')
		# return float(pair.substr(pair+1))
	except:
		return np.nan
	


def read_config(
		filename,
		keys_map = CONFIG_KEYS_MAP,
		default = CONSTS_DEFAULT,
	):
	
	cfg = {}

	# read the actual config file into a dict
	with open(filename, 'r') as fin:
		for line in fin:
			# expected line format:
			# <key> = <value>
			# should work w/ any whitespace
			key, _, val = line.split()

			cfg[key] = val

#	# map keys if needed
#	if keys_map is not None:
#		cfg = {
#			keys_map[k] : cfg[k]
#			for k in cfg
#		}

	# change type
	if default is not None:
		cfg = {
			k : type(default[k])(cfg[k])
			for k in cfg		
		}

	# read ID from filename
	# cfg['CONFIG_ID'] = filename[
	# 	- ( LEN_ID + 1 + len('config.txt') ) 
	# 	: - ( len('config.txt') + 1 )
	# ]

	return cfg



def read_single_folder(d, keys_map = CONFIG_KEYS_MAP) -> Dict[str, Any]:
	data = read_config(d + 'config.txt', keys_map = keys_map)

	for c in LOSS_TYPES:
		data[c] = read_loss(d + 'loss.txt', LOSS_TYPES[c])

	if ENABLE_TESTING_DATA:
		data['TEST_ACCURACY'] = read_percent(d + 'percent0.txt')
	
	# print('\t%s' % str(data))		
	return data



def read_all_data(datadir = '../../../psweep_data/', rem_cols = None, run_ID = ''):
	# get directories
	# dirnames = [join(datadir, f) + '/' for f in listdir(datadir) if isdir(join(datadir, f)) and f[0] == sys.argv[1][0]]
	dirnames = [ x + '/' for x in glob.glob(datadir + run_ID + '_*') if isdir(x) ]
	
	n_total_dir = len(dirnames)
	print('> directories found:\t%d\n' % n_total_dir)

	# get columns
	cols = CONSTS_DEFAULT_KEYS + [ s for s in LOSS_TYPES ]
	if ENABLE_TESTING_DATA:
		cols = cols + ['TEST_ACCURACY']

	# read in data
	data = []
	i = 0
	for d in dirnames:
		print('\t read: \t%d\t/\t%d' % (i,n_total_dir), end='\r')
		data.append(read_single_folder(d))
		i = i + 1

	print('\n\n> directories read in:\t%d' % len(data))

	# bulk write to dataframe
	# df = pd.DataFrame( columns = cols )
	# df = df.append(data, ignore_index = True)
	# df = df.append(data)
	df = pd.DataFrame(data)

	# remove some columns with junk
	if rem_cols is not None:
		for r in rem_cols:
			del df[r]

	return df	


def read_and_save(filename, datadir = '../../../psweep_data/', rem_cols = None, run_ID = ''):
	df = read_all_data(datadir, rem_cols, run_ID)
	df.to_pickle(filename)

	return df


def main(argv = sys.argv):
	datadir = None

	if len(argv) > 1:
		run_ID = argv[1]
	else:
		run_ID = ''

	if len(argv) > 2:
		datadir = argv[2]
	else:
		datadir = '../../../psweep_data/'

	filename = 'data_%s.df' % run_ID
	
	print('filename=\t%s\ndatadir=\t%s\nrun_ID=\t%s' % (filename, datadir, run_ID))

	read_and_save(filename, datadir, rem_cols = None, run_ID = run_ID)

if __name__ == "__main__":
	main(sys.argv)
	
