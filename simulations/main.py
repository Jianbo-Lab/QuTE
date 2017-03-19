from experiment import *
import argparse
import numpy as np
import os
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--variable',type = str,default = 'p')
	parser.add_argument('--pi1',type = float,default = 0.3)
	parser.add_argument('--n_samples',type = int,default = 1000)
	parser.add_argument('--p',type = float,default = 0.5)
	parser.add_argument('--p1',type = float,default = 0.9)
	parser.add_argument('--p2',type = float,default = 0.1)
	parser.add_argument('--d',type = int, default = 32)
	parser.add_argument('--mu',type = float,default = 2) 
	parser.add_argument('--alpha',type= float,default = 0.2) 
	parser.add_argument('--replicate',type = int, default = 100)
	parser.add_argument('--var_start',type = float,default = 0.9)
	parser.add_argument('--var_stop',type = float,default = 0.999)
	parser.add_argument('--var_step',type = float,default = 0.01)
	# parser.add_argument('--add_classical',type = int, 
	# 	default = 0, choices = [0,1]) 
	parser.add_argument('--experiment',type = str,
		default = '1', choices = ['1','2','plot1','plot2','3','plot3','4','plot4','5','plot5'])
 

	args = parser.parse_args()   

	var_range = np.arange(args.var_start,args.var_stop,args.var_step)

	# add_classical = False if args.add_classical == 0 else True

	if args.experiment == '1': 
		output = experiment1(args.variable,
			var_range,
			args.pi1,
			args.n_samples,
			args.p,
			mu=args.mu,
			alpha=args.alpha,
			replicate=args.replicate) 

	elif args.experiment == '2':
		output = experiment2_with_expander(variable = args.variable,
			var_range = var_range,
			pi1 = args.pi1,
			n_samples = args.n_samples, 
			p = args.p, 
			mu = args.mu,
			alpha = args.alpha,
			replicate = args.replicate)
	elif args.experiment == '3':
		output = experiment3_with_regular(variable = args.variable,
			var_range = var_range,
			pi1 = args.pi1,
			n_samples = args.n_samples, 
			d = args.d, 
			mu = args.mu,
			alpha = args.alpha,
			replicate = args.replicate)

	elif args.experiment == 'plot1':
		path1 = "results/experiment1/"
		for file in os.listdir(path1):
			if file.endswith(".save.npy"):
				plot_wrt_output_experiment1(path1, file)

	elif args.experiment == 'plot2':
		path2 = "results/experiment2/"
		for file in os.listdir(path2):
			if file.endswith(".save.npy"):
				plot_wrt_output_experiment2(path2, file)

	elif args.experiment == 'plot3':
		path3 = "results/experiment3/"
		for file in os.listdir(path3):
			if file.endswith(".save.npy"):
				plot_wrt_output_experiment3(path3, file)

	elif args.experiment == '4':
		output = experiment4_with_SBM(variable = args.variable,
			var_range = var_range,
			pi1 = args.pi1,
			n_samples = args.n_samples, 
			p1 = args.p1,
			p2 = args.p2, 
			mu = args.mu,
			alpha = args.alpha,
			replicate = args.replicate)		
	elif args.experiment == 'plot4':
		path4 = "results/experiment4/"
		for file in os.listdir(path4):
			if file.endswith(".save.npy"):
				plot_wrt_output_experiment4(path4, file)

	elif args.experiment == '5':
		output = experiment5_with_lattice(variable = 'r',
			var_range = np.arange(1,16,1),
			pi1 = args.pi1, 
			r = 1,
			generator = gt.lattice,
			mu = 2,
			alpha = 0.2,
			replicate = args.replicate, 
			path = 'results/experiment5/')	

	elif args.experiment == 'plot5':
		path5 = "results/experiment5/"
		for file in os.listdir(path5):
			if file.endswith(".save.npy"):
				plot_wrt_output_experiment5(path5, file)

if __name__ =='__main__':
	main()