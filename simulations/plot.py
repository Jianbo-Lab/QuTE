import matplotlib.pyplot as plt
import matplotlib
import numpy as np
font = {'family' : 'normal',
		'weight' : 'bold',
		'size'   : 22}

matplotlib.rc('font', **font)

def map_to_latex(variable, simplified = False):
	if simplified:
		if variable == 'pi1':
			return r'$\pi_1$'
		elif variable  == 'mu':
			return r'$\mu$'
		elif variable  == 'p':
			return 'p'
		elif variable == 'd':
			return 'd'
	else:
		if variable == 'p':
			variable_in_word = 'p, for G(1000,p)'
		elif variable == 'pi1':
			variable_in_word = r'Proportion $\pi_1$ of $H_1$'
		elif variable == 'mu':
			variable_in_word = r'Mean $\mu$ of $N(\mu,1)$ in $H_1$'
		elif variable == 'd':
			variable_in_word = 'Degree d of each node'
		elif variable == 'p1':
			variable_in_word = r'Within-block probability $p_1$'

		return variable_in_word 
 

def plot_gnp_single(x,y,yerr, title, xlabel, ylabel, name, add_classical,
		  graphtype='power'):
	"""
	This function plots the figure with error bar 

	and save it to local.
	"""
	plt.rc('text', usetex = True)
	plt.rc('font', family = 'serif')
	if add_classical:
		fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (10,8)) 
		ax.errorbar(x,y[:,0],marker='o',yerr = yerr[:,0], label = 'QuTE',color='red')
		ax.errorbar(x,y[:,1],marker='o',yerr = yerr[:,1], label = 'Bonferroni',color='blue')
		ax.errorbar(x,y[:,2],marker='o',yerr = yerr[:,2], label = 'BH',color='green')
	
		if not graphtype == 'power':
			plt.plot(np.array([0,1]),np.array([0.2,0.2]), 
				 linestyle='dashed',
				 label = 'Targeted FDR',
				color='black')
			
		ax.legend(loc = 'upper right',fontsize = 22)
		ax.set_title(title)
		ax.set_xlabel(xlabel,fontsize = 28)
		ax.set_ylabel(ylabel,fontsize = 28)
		ax.set_ylim(bottom = 0,top=1)
		plt.savefig(name, format='png', dpi=200)
	else:
		fig, ax = plt.subplots(nrows = 1, ncols = 1) 
		ax.errorbar(x,y,yerr = yerr)
		ax.set_title(title)
		ax.set_xlabel(xlabel,fontsize = 28)
		ax.set_ylabel(ylabel,fontsize = 28)
		ax.set_ylim(bottom = 0,top=1)
		plt.savefig(name, format='png', dpi=200)		


def plot_gnp(path, saved_file):
	output = np.load(path + saved_file)
	subtitle = saved_file.split('_')[0]
	_,variable,var1_name,var1,var2_name,var2,_,rep = subtitle.split('-')

	y_fdr, yerr_fdr,y_pow,yerr_pow = \
	output[:,:,0],output[:,:,1], output[:,:,2], output[:,:,3]
	var_range = output[:,0,4] 

	variable_in_word = map_to_latex(variable) 

	plot_gnp_single(x=var_range,y=y_fdr,yerr=yerr_fdr,
		title = r'FDR v.s. {}'.format(variable_in_word), 
		xlabel = variable_in_word,
		ylabel = r'Achieved FDR',
		name = 'results/figures/FDR-Vary-p-rep-{}.png'.format(rep), 
		add_classical = True,
		 graphtype='FDR') 

	plot_gnp_single(x=var_range,y=y_pow,yerr=yerr_pow,
		title = r'Power v.s. {}'.format(variable_in_word),
		xlabel = variable_in_word,
		ylabel = r'Power',
		name = 'results/figures/Power-Vary-p-rep-{}.png'.format(rep), 
		 add_classical = True,
		 graphtype='power') 
	
def plot_grid_single(x,y,yerr, title, xlabel, ylabel, name, graphtype = 'power'):
	"""
	This function plots the figure with error bar 

	and save it to local.
	"""
	plt.rc('text', usetex = True)
	plt.rc('font', family = 'serif') 
	fig, ax = plt.subplots(nrows = 1, ncols = 1,
						   figsize=(10,8)) 
	if not graphtype == 'power':
		plt.plot(np.array([1,15]),np.array([0.2,0.2]), 
				 linestyle='dashed',
				label = 'Targeted FDR',
				color = 'black')
	ax.errorbar(x,y[:,0],
		yerr = yerr[:,0], 
		marker = 'o',
		label = 'QuTE for rectangle graph',
		color='red')
	ax.errorbar(x,y[:,3],
		yerr = yerr[:,3], 
		marker = 'o', 
		label = 'QuTE for square graph',
		color='darkorange')
	ax.errorbar(x,y[:,1],
		yerr = yerr[:,1], 
		marker = 'o', 
		label = 'Bonferroni',
		color = 'blue')
	ax.errorbar(x,y[:,2],
		yerr = yerr[:,2], 
		marker = 'o', 
		label = 'BH',
		color = 'green')
	


	ax.legend(loc='upper right',fontsize=18)
	ax.set_title(title)
	ax.set_xlabel(xlabel,fontsize=28)
	ax.set_ylabel(ylabel,fontsize=28)
	if graphtype == 'power':
		ax.set_ylim(bottom = 0,top=1)
	else:
		ax.set_ylim(bottom = 0,top=1)
	plt.savefig(name, format='png', dpi=200) 	

def plot_grid(path, saved_file):
	output = np.load(path + saved_file)
	subtitle = saved_file.split('_')[0] 
	_,_,_,pi1,_,mu,_,rep,_ = subtitle.split('-')

	y_fdr, yerr_fdr,y_pow,yerr_pow = \
	output[:,:,0],output[:,:,1], output[:,:,2], output[:,:,3]

	var_range = output[:,0,4] 

	variable_in_word = 'Rounds of Communication c' 

	plot_grid_single(x=var_range,y=y_fdr,yerr=yerr_fdr,
		title = r'FDR v.s. Communication, for Grid Graph',
		xlabel = variable_in_word,
		ylabel = r'Achieved FDR',
		name = 'results/figures/FDR-Vary-c-grid-rep-{}.png'.format(rep),
		 graphtype='fdr') 

	plot_grid_single(x=var_range,y=y_pow,yerr=yerr_pow,
		title = r'Power v.s. Communication, for Grid Graph',
		xlabel = variable_in_word,
		ylabel = r'Power',
		name = 'results/figures/Power-Vary-c-grid-rep-{}.png'.format(rep),
		 graphtype='power') 

