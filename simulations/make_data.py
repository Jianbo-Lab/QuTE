from numpy.random import randint, poisson
import numpy as np 
import graph_tool.all as gt
from scipy.stats import norm
from collections import Counter
class Data(object):
	"""
	Each instance of Data has an undirected graph,
	each node of which is associated with a hypothesis. 

	Null H0: z~N(0,1)
	Alternative H1: z~N(mu,1)

	Each node is also associated with a 0/1 indicating whether the hypothesis 
	is H0 or H1.

	Each node is also associated with a p-value calculated by 1-Phi(z).  

	The node is numbered as 0,...,n. So we will use two arrays 
	to store the above two quantities. 

	"""
	def __init__(self, pi1, 
		params, 
		generator, 
		mu, 
		seed,
		block = False):
		"""
		Inputs:
		pi1: proportion of H1.

		params: A dictionary storing parameters for generating a random graph.

		generator: random graph generator.

		mu: mean of Z in H1.

		seed: random seed.

		block: indicating if data is generated from a SBM.
		"""

		self.pi1 = pi1 
		self.params = params
		self.generator = generator
		self.mu = mu 
		self.seed = seed
		self.block = block

		self._generate_graph()
		
		nodes_val = self._generate_rv(self.n_nodes) 
 
		self.p_vals = nodes_val[:,0]
		self.hypos = nodes_val[:,1].astype(np.bool) 

		self.ifreject = None
		

	def _generate_graph(self):
		np.random.seed(self.seed)
		gt.seed_rng(self.seed)
		if 'block_membership' in self.params and self.params['block_membership'] != None:
			self.graph, self.bm = self.generator(**self.params) 
		else:
			self.graph = self.generator(**self.params) 
		self.n_nodes = self.graph.num_vertices()

	def _generate_rv(self, n_samples):
		np.random.seed(self.seed)

		all_samples = np.random.randn(n_samples)

		num_nulls = int((1-self.pi1) * n_samples) + np.random.randint(2) 

		null = all_samples[:num_nulls] 
		alternative = all_samples[num_nulls:] + self.mu

		p_null = 1 - norm.cdf(null)
		p_alter = 1 - norm.cdf(alternative)


		null_nodes_val = np.array([p_null,np.zeros(p_null.shape)]).T
		alter_nodes_val = np.array([p_alter,np.ones(p_alter.shape)]).T
 
		nodes_val = np.vstack((null_nodes_val,alter_nodes_val))

		if not self.block:
			# randomly permutes data to avoid patterns from matching indices.
			nodes_val = np.random.permutation(nodes_val)
		elif self.block == 'concentrated':
			block_inds = self.bm.get_array()

			inds_in_order = [np.argwhere(block_inds == i) for i in set(block_inds)] 
			
			counter = Counter(self.bm.get_array())
			num_samples_each_class = counter.values() 
			classes = counter.keys() 

			# Find the maximum number of blocks nulls concentrated.
			k = 0
			current = 0
			nodes_val = np.zeros(nodes_val.shape)
			while current < num_nulls:
				current += num_samples_each_class[k]
				k += 1
			k -= 1 
			# At class k, part of hypo is null and part of hypo is alternative.
			num_alters_at_k = current - num_nulls
			num_nulls_at_k = num_samples_each_class[k] - num_alters_at_k

			null_inds = np.concatenate(inds_in_order[:k])
			null_inds = np.concatenate([null_inds,
				inds_in_order[k][:num_nulls_at_k]]) 

			alter_inds = inds_in_order[k][num_nulls_at_k:]
 
			alter_inds = np.concatenate([alter_inds] + inds_in_order[k+1:])
 
			nodes_val[null_inds.reshape(-1),:] = null_nodes_val
			nodes_val[alter_inds.reshape(-1),:] = alter_nodes_val

		return nodes_val
 



