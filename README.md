# QuTE

Code for reproducing key results in the paper [QuTE algorithms for decentralized decision making on networks with false discovery rate control](https://github.com/Jianbo-Lab/QuTE) by Aaditya Ramdas, Jianbo Chen, Martin J. Wainwright, Michael I. Jordan.


## Dependencies

This project was written in Python. It currently requires the package graph_tool of version 2.22 available on https://graph-tool.skewed.de. 

In addition, please 'pip install' the following packages: 
- `numpy`
- `scipy`

## Running Experiment

We provide the source code to replicate the simulations:

```bash
cd simulations/
python run_simulation.py
```

We also provide the source code to replicate our experiment on Intel Lab Data:

```bash
cd applications/
python run_real_data.py
```