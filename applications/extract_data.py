import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  
import urllib2 
import gzip
import StringIO
from utils import detrend

def extract_data(): 
	response = urllib2.urlopen('http://db.csail.mit.edu/labdata/data.txt.gz') 
	compressedFile = StringIO.StringIO()
	compressedFile.write(response.read()) 
	compressedFile.seek(0) 
	decompressedFile = gzip.GzipFile(fileobj=compressedFile, mode='rb')
	html = decompressedFile.read()
	lines = html.split('\n')
	lines = [line.split(' ')[2:] for line in lines][:-1] 

	data = pd.DataFrame(lines, columns=['epoch','moteid',
										'temperature','humidity',
										'light','voltage'])
	data = data.apply(pd.to_numeric) 
	data = data.dropna(axis = 0) 
	data = data[data['voltage']>0] 
	# Select epoches with more than 40 motes per epoch. 
	data=data.groupby([data['epoch']//100]).\
	filter(lambda x: x['moteid'].nunique()>= 40) 
	return data

def average_data(data):
	"""
	Take means every 100 epochs. 
	""" 
	data['count'] = data['temperature'].copy() 
	data.columns = ['epoch','moteid','temperature_mean',
					'humidity_mean','light_mean', 
					'voltage', 'count'] 
	averaged_data = data.groupby([data['epoch']//100, data['moteid']]).\
	agg({'temperature_mean': np.mean, 
		 'humidity_mean': np.mean, 
		 'light_mean': np.mean,
		 'voltage':np.mean,
		'count': len}) 
	# Include epoch, moteid as two columns.
	averaged_data.reset_index(inplace=True) 
	return averaged_data
 
def detrend_data(averaged_data):
	"""
	Detrend the time series, taking away long-term effects.
	"""
	detrended_data = averaged_data.copy()
	for moteid in range(1, 59):
		for feature in ['temperature_mean','humidity_mean']:
			if moteid not in [5,15,28,57]: 
				detrended_data.loc[detrended_data['moteid']==moteid,feature]=\
				detrend(averaged_data, moteid,feature)
	return detrended_data

def pivot_data(detrended_data):
	grouped_by_id = detrended_data.groupby('moteid').mean()

	mean_by_epoch = detrended_data.pivot(index = 'epoch', 
						   columns = 'moteid',
						   values ='temperature_mean')  
	columns = mean_by_epoch.columns.copy()

	# Fill in NA values:
	for i in columns:
		mean_by_epoch[i].fillna(value = grouped_by_id.loc[i,'temperature_mean'],
							inplace = True)  

	return mean_by_epoch,columns

def extract_coordinates():
	response = urllib2.urlopen('http://db.csail.mit.edu/labdata/mote_locs.txt')
	html = response.read()
	lines = html.split('\n')
	lines = [line.split(' ') for line in lines][:-1]
	coordinates = [np.array([float(line[1]),float(line[2])]) for line in lines]
	return coordinates

def extract_connectivity():
	response = urllib2.urlopen('http://db.csail.mit.edu/labdata/connectivity.txt')
	html = response.read()
	lines = html.split('\n')
	lines = [line.split(' ')[1:] for line in lines][:-2] 
	for i,line in enumerate(lines):
		if line[2]=='':
			lines[i][2]='0'

	return lines
 


