import sys 
sys.path.append('..') 
import numpy as np
import random
from scipy.stats import norm
from make_data import Data
from algorithm import generalized_BH, get_1_neighbours, get_c_neighbours
from utils import estimate_fdr_and_power,estimate_fdr_and_power_with_arrays  
import statsmodels.sandbox.stats.multicomp 
import graph_tool.all as gt
from numpy.random import randint,poisson
def run_single_experiment(pi1,params,generator,mu,
	alpha = 0.2,
	replicate = 10,
	add_classical = False, 
	block = False,
	get_nbhd = get_1_neighbours):
	"""
	This function carries out an experiment with the same 
	hyperparameters with number of replications.

	Input: 
	pi1: proportion of H1.

	params: A dictionary storing parameters for generating a random graph.

	generator: random graph generator.

	mu: mean of Z in H1.

	add_classical: whether we carry out BH and Bonferroni simultaneously.

	blcok: Whether we use a stochastic block model

	Output: 
	If add_classical, returns a [3,4]-dim array.

	Each row collects statistics of QuTE, Bonferroni, BH respectively. 
	Each column is the mean of fdr, sd of fdr, mean of power and sd of power
	respectively.

	If not add_classical, returns a 4-dim array,
	recording mean, sd of fdr and mean, sd of power.

	"""
	fdrs = np.zeros((replicate,3)) if add_classical else np.zeros(replicate)  
	powers = np.zeros((replicate,3)) if add_classical else np.zeros(replicate)  

	for seed in range(replicate):

		# Generate Data.
		sample = Data(pi1,params,generator,mu,seed, block = block)

		if add_classical:
			# Carry out the algorithm.
			generalized_BH(sample,alpha, get_nbhd = get_nbhd)

			# Truth
			hypo = sample.hypos

			# Rejections got from built-in algorithms.
			p_vals = sample.p_vals
			
			bon_rejections = statsmodels.sandbox.stats.multicomp.\
			multipletests(p_vals,alpha,'bonferroni')[0]
			bh_rejections = statsmodels.sandbox.stats.multicomp.\
			multipletests(p_vals,alpha,'fdr_bh')[0]

			# Estimate fdr and power. 
			fdrs[seed,0], powers[seed,0] = estimate_fdr_and_power(sample)
			fdrs[seed,1], powers[seed,1] = estimate_fdr_and_power_with_arrays(bon_rejections, hypo)
			fdrs[seed,2], powers[seed,2] = estimate_fdr_and_power_with_arrays(bh_rejections, hypo)
		else:
			# Carry out the algorithm.
			generalized_BH(sample,alpha, get_nbhd = get_nbhd)			

			# Estimate fdr and power. 
			fdrs[seed], powers[seed] = estimate_fdr_and_power(sample)
	if add_classical:
		output = np.zeros((3,4))
		output[:,0] = np.mean(fdrs,axis = 0)
		output[:,1] = np.std(fdrs,axis = 0)
		output[:,2] = np.mean(powers,axis = 0)
		output[:,3] = np.std(powers,axis = 0)

		return output
	else:
		return np.array([np.mean(fdrs), np.std(fdrs), np.mean(powers), np.std(powers)])

def experiment_on_gnp(variable = 'p',
	var_range = np.arange(0.1,1.1,0.1),
	pi1 = 0.3,
	n_samples = 1000, 
	p = 0.5,
	generator = gt.random_graph,
	mu = 2,
	alpha = 0.2,
	replicate = 100, 
	path = 'results/gnp/'):
	"""
	This function varies variable in var_range
	while controls other hyperparameters.

	Output: 

	An array of size [len(var_range),4] storing data.
	The array is also saved to path. 
	"""
	output = np.zeros((len(var_range), 3, 4))

	for i,var in enumerate(var_range):
		if variable == 'p':
			p = var
		elif variable == 'mu':
			mu = var
		elif variable == 'pi1':
			pi1 = var

		params = {'N':n_samples,
		'deg_sampler':lambda: poisson((n_samples-1)*p),
		'directed': False,
		'block_membership': None,
		'model': 'erdos'}
		output[i] = run_single_experiment(pi1,params,generator,\
			mu,alpha,replicate,add_classical = True)	

	if variable == 'p':
		subtitle = 'vary-p-pi1-{}-mu-{}-rep-{}'.format(pi1,mu,replicate) 

	output = np.concatenate((output,np.tile(var_range,(1,3,1)).T),2)

	np.save(path + subtitle + '_output.save',output)
	return output

	
def experiment_on_grid(variable = 'c',
	var_range = np.arange(10,20,1),
	pi1 = 0.25, 
	c = 1,
	generator = gt.lattice,
	mu = 2,
	alpha = 0.2,
	replicate = 10, 
	path = 'results/grid/'):
	"""
	This function varies variable in var_range
	while controls other hyperparameters.

	Output: 

	An array of size [len(var_range),4, 4] storing data.
	The array is also saved to local. 

	The output array is arranged in such a form:
	[variable range, type (which line), (fdr,fdr_err,pow,pow_err)]
	type is ordered as QuTE on rectangle graph, Bonferroni, BH and
	QuTE on square graph respectively.

	""" 
	output = np.zeros((len(var_range), 4, 4))
 
	for i,var in enumerate(var_range):
		if variable == 'c':
			c = var 

		width,length = 2, 128
		output[i,:3,:] = run_single_experiment(pi1,
			{'shape':[width,length]},
			generator, 
			mu,alpha,replicate,
			add_classical = True,
			get_nbhd = lambda graph, i: \
			get_c_neighbours(graph, i, c, length-1,width-1))	

		width,length = 16,16
		output[i,3,:] = run_single_experiment(pi1,
			{'shape':[width,length]},
			generator, 
			mu,alpha,replicate,
			add_classical = False,
			get_nbhd = lambda graph, i: \
			get_c_neighbours(graph, i, c, length-1,width-1))	

	if variable == 'c':
		subtitle = 'vary-c-pi1-{}-mu-{}-rep-{}-lattice'.format(pi1,mu,replicate)
 
	output = np.concatenate((output,np.tile(var_range,(1,4,1)).T),2)

	np.save(path + subtitle + '_output.save',output)
	return output
 