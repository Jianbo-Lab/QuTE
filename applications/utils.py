import graph_tool.all as gt 
import numpy as np 
import pandas as pd
from sklearn.linear_model import LinearRegression 
from scipy.stats import percentileofscore
def detrend(averaged_data, moteid, feature): 
	X = averaged_data[averaged_data['moteid']==moteid]['epoch'].values
	y = averaged_data[averaged_data['moteid']==moteid][feature].values
	model = LinearRegression()
	model.fit(X.reshape(-1,1), y.reshape(-1,1))
	# # calculate trend
	trend = model.predict(X.reshape(-1,1)) 
	# # detrend
	detrended = y - trend.reshape(-1) 
	return detrended

def calculate_p_values(mean_by_epoch, columns):
	"""
	Calculate the p values of a specific epoch.
	"""
	middle_epoch = 500
	pvalues = np.zeros(len(columns))
	for i in range(len(columns)):
		column = columns[i]
		first_part_rvs = mean_by_epoch[column][:middle_epoch].values
		score = mean_by_epoch[column][middle_epoch+15] 
		p_prev = percentileofscore(first_part_rvs, score) / 100.0
		pvalues[i] = 2 * min(1- p_prev, p_prev)
	return pvalues

def construct_graph(adj_matrix):
	g = gt.Graph(directed=False)
	num_v = len(adj_matrix)
	g.add_vertex(n = num_v)

	rowids,colids = np.where(adj_matrix == 1)
	edge_list = zip(rowids,colids)
	g.add_edge_list(edge_list = edge_list) 
	return g

def add_position_map(g,coordinates):
	position = g.new_vertex_property("vector<double>")
	for i in range(54):
		position[g.vertex(i)] = coordinates[i]
		
	return position

def generate_adj(gamma, lines):  
	adj_matrix = np.tile(0,(54,54))
	for line in lines[:-1]:
		i = int(line[0])-1
		j = int(line[1])-1
		adj_matrix[i,j] = int(float(line[2])>gamma)

	for i in range(54):
		for j in range(54):
			adj_matrix[i,j] = int(adj_matrix[i,j] and adj_matrix[j,i])

	for i in range(54):
		for j in range(54):
			if i <= j:
				adj_matrix[i,j] = 0
				
	return adj_matrix 

def add_color_map(g,rejections):
	red_blue_map = {'red':(1,0,0,1),'blue':(0,0,1,1)}
	colors = g.new_vertex_property("vector<double>")
	for j in range(54):
		colors[g.vertex(j)] = red_blue_map['red'] if rejections[j] else \
		red_blue_map['blue']
	return colors

