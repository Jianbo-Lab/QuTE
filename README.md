# QuTE

Code for reproducing key results in the paper [QuTE algorithms for decentralized decision making on networks with false discovery rate control](https://github.com/Jianbo-Lab/QuTE) by Aaditya Ramdas, Jianbo Chen, Martin J. Wainwright, Michael I. Jordan.


## Dependencies

This project was written in Python. It currently requires the package graph_tool of version 2.22 available on https://graph-tool.skewed.de. 

In addition, please 'pip install' the following packages: 
- `numpy`
- `scipy`
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
python run_simulations.py --replicate 10 --experiment plot_gnp

# Plot figures for the second experiment on grid graphs.
python run_simulations.py --replicate 10 --experiment plot_grid
```
Data and plots used in our paper use 1,000 replications. The figures can be found in results/figures. 

We also provide the source code to replicate our experiment on Intel Lab Data:

```bash
cd applications/
python run_real_data.py
```