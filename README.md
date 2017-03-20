# QuTE

Code for reproducing key results in the paper [QuTE algorithms for decentralized decision making on networks with false discovery rate control](https://github.com/Jianbo-Lab/QuTE) by Aaditya Ramdas, Jianbo Chen, Martin J. Wainwright, Michael I. Jordan.


## Dependencies

This project was written in Python 2.7. It currently requires the package graph_tool of version 2.22 available on https://graph-tool.skewed.de. 

In addition, please 'pip install' the following packages: 
- `numpy`
- `scipy`
- `pandas`
- `statsmodels`
- `matplotlib`

## Running Experiment

We provide the source code to replicate the simulations:

```bash
cd simulations/
# A test run of the first experiment on G(n,p)
python run_simulations.py --replicate 10 --experiment gnp

# A test run of the second experiment on grid graphs.
python run_simulations.py --replicate 10 --experiment grid

# The figures can only be plotted after the corresponding experiment has been run.
# Plot figures for the first experiment on G(n,p).
python run_simulations.py --experiment plot_gnp

# Plot figures for the second experiment on grid graphs.
python run_simulations.py --experiment plot_grid
```
Data and plots used in our paper use 1,000 replications. Below we plot the results from two experiments here. The figures can also be found in simulations/results/figures.  

![Alt text](https://github.com/Jianbo-Lab/QuTE/blob/master/simulations/results/figures/FDR-Vary-p-rep-1000.png) ![Alt text](https://github.com/Jianbo-Lab/QuTE/blob/master/simulations/results/figures/Power-Vary-p-rep-1000.png)

![Alt text](https://github.com/Jianbo-Lab/QuTE/blob/master/simulations/results/figures/FDR-Vary-c-grid-rep-1000.png) ![Alt text](https://github.com/Jianbo-Lab/QuTE/blob/master/simulations/results/figures/Power-Vary-c-grid-rep-1000.png)

We also provide the source code to replicate our experiment on Intel Lab Data:

```bash
# Extract and clean the real data, run QuTE and generate the three figures.
cd applications/
python run_real_data.py
```
Below are three generated figuers with threshold on communication probability being 0.1, 0.3, 0.5 respectively. The figures can also be found in applications/results. Details can be found in our paper.

![Alt text](https://github.com/Jianbo-Lab/QuTE/blob/master/applications/results/sensor-graph-threshold-0.1.png) ![Alt text](https://github.com/Jianbo-Lab/QuTE/blob/master/applications/results/sensor-graph-threshold-0.3.png) ![Alt text](https://github.com/Jianbo-Lab/QuTE/blob/master/applications/results/sensor-graph-threshold-0.5.png)

