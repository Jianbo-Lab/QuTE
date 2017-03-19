import matplotlib.pyplot as plt 
from extract_data import *
from utils import *
import sys
sys.path.append('../')
from algorithm import * 
def main():
	# Extract raw measurements from Intel Lab data.
	data = extract_data()

	# Average over consecutive 100 epochs.
	averaged_data = average_data(data)

	# Detrend the data.
	detrended_data = detrend_data(averaged_data)

	# Pivot the data by Mote Ids.
	mean_by_epoch, columns = pivot_data(detrended_data)

	# Calculate p-values. 
	pvalues = calculate_p_values(mean_by_epoch, columns)

	# Extract coordinates of each mote.
	coordinates = extract_coordinates()

	# Extract communication probability of each two motes.
	connectivity = extract_connectivity()

	# Gamma is the threshold over communication probability. 
	for x,gamma in enumerate([0.1,0.3,0.5]):
		# Carry out QuTE based on extracted graph and p values.
		adj_matrix = generate_adj(gamma, connectivity)
		g = construct_graph(adj_matrix)
		position = add_position_map(g,coordinates) 

		rejections = generalized_BH_original(g,pvalues,0.05) 
		rejections = np.concatenate((rejections[:4],
									np.array([False]),
									rejections[4:26],
									np.array([False]),
									rejections[26:54]))[:54]

		# Plot rejections on a graph. Red: Rejected. Blue: Not rejected.
		gt.graph_draw(g, pos = position,  
				  vertex_fill_color = add_color_map(g,rejections),
				 output='results/sensor-graph-threshold-{}.png'.format(gamma))

if __name__ == '__main__':
	main()