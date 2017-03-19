import os
from experiment import *
from plot import *
import argparse
import numpy as np
import os
def main():
	parser = argparse.ArgumentParser() 
	parser.add_argument('--replicate',type = int, default = 1000) 
	parser.add_argument('--experiment',type = str,
		default = 'gnp', choices = ['gnp','grid','plot_gnp','plot_grid'])
 

	args = parser.parse_args()     

	if args.experiment == 'gnp': 
		output = experiment_on_gnp('p',
			np.arange(0,1.05,0.05), 0.3, 1000, 0,
			mu=2,
			alpha=0.2,
			replicate=args.replicate) 

	elif args.experiment == 'grid':
		output = experiment_on_grid(variable = 'c',
			var_range = np.arange(1,16,1),
			pi1 = 0.3, c = 1, generator = gt.lattice, mu = 2, alpha = 0.2,
			replicate = args.replicate)

	elif args.experiment == 'plot_gnp':
		path = "results/gnp/"
		for file in os.listdir(path):
			if file.endswith(".save.npy"):
				plot_gnp(path, file)

	elif args.experiment == 'plot_grid':
		path = "results/grid/"
		for file in os.listdir(path):
			if file.endswith(".save.npy"):
				plot_grid(path, file)

if __name__ == '__main__':
	main()
