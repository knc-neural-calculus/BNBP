import os
import sys
import numpy as np
import matplotlib.pyplot as plt



def load_voltage_traces(filename):
	filetype = filename.split('.')[-1]
	data = None
	if filetype in ['npy', 'npz']:
		data = np.load(filename)['arr_0']
	elif filetype == 'csv':
		data = np.genfromtxt(filename, delimiter=',').T


	data = data[:-1]
	# data = data[:,00000:100000]
	# data = data[:,1400000:]
	
	return data


def spiketrain_from_vts(vts, threshold = 20.0, maxlength = 30.0):	
	# output = np.where(voltage_trace > 20.0, 1, 0)
	print(vts.shape)
	
	output = []
	for x in vts:
		output.append(np.where(x > 20.0)[0])

	return output


def plot_vt(filename_vt, run_cfg = ''):
	vts = load_voltage_traces(filename_vt)
	data = spiketrain_from_vts(vts)

	# plot voltage trace
	for x in vts:
		plt.plot(x)

	# plot raster, offset
	for i,x in enumerate(data):
		plt.plot(
			x,
			np.full(
				len(x),
				2 * i - ( 2 * len(data) + 50 ),
			),
			'b.'
		)

	figure_filename = run_cfg + filename_vt.split('.')[0] + '_plot.png'
	plt.savefig(figure_filename)

	# plt.show()

def main(dirname):
	run_cfg = dirname.split('/')[-1]

	plot_vt(dirname + 'X1_voltages.csv', run_cfg)
	plot_vt(dirname + 'X2_voltages.csv', run_cfg)
	

if __name__ == "__main__":
	main(sys.argv[1])