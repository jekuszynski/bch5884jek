#!/usr/bin/env python3
#https://github.com/jekuszynski/bch5884jek/blob/master/assignments/project_2/sec_peak_finder.py

#importing all required modules
import sys
import numpy as np
from matplotlib import pyplot as plt

#open and parse the given file
f=open("superose6_50.asc")
lines=f.readlines()
f.close()

time=[]
sig=[]

for line in lines[3:]:
	words=line.split()
	try:
		time.append(float(words[0]))
		sig.append(float(words[1]))
	except:
		continue

time=np.array(time)
sig=np.array(sig)
dsig=np.gradient(sig)
ddsig=np.gradient(dsig)

print(time)

tpeaks=[]

def find_local_minima(arr,thr=5,noise=.1,target=tpeaks):
	for t in range(len(arr)):
		try:
			prev_min = arr[t-int(thr):t-1].min()
			next_min = arr[t+1:t+int(thr)].min()
		except ValueError:
			#exception handling for when trying to take a minimum of an empty array
			prev_min = np.zeros(thr).min()
			next_min = np.zeros(thr).min()
		'''if a point on the 2nd derivative plot is less than the values ahead 
		and before it by the given variable "thr", then it will be added to the
		new array for future processing. Otherwise it will be giving a nan.'''
		if arr[t] < prev_min and arr[t] < next_min and np.abs(arr[t]) > float(noise):
			target.append(arr[t])
		else:
			target.append(np.nan)
			continue

find_local_minima(ddsig,20,.5)
peak_list=[]

def find_peak_times(arr_t,arr_peaks=tpeaks):
	for t in range(len(arr_peaks)), range(len(arr_t)):
		if isinstance(arr_peaks[t],float):
			peak_list.append(arr_t[t])
		else:
			continue

find_peak_times(time)
print(peak_list)

# def find_peak_area(arr, ref=peak_list):
# 	for t in range(len(arr)):
# 		if arr[t] == any(ref):
# 			asdfasdf
# 			asdfasdf
			#first/2nd derv here? Find width so long as the slope is decreasing?


plt.plot(time,tpeaks,'o')
plt.plot(time,sig)
plt.plot(time,ddsig)
plt.xlim(0,165)
plt.ylim(-15,1000)
plt.show()
plt.plot(time,tpeaks,'o')
plt.plot(time,ddsig)
plt.xlim(0,165)
plt.ylim(-15,20)
plt.show()