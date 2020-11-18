#!/usr/bin/env python3
#https://github.com/jekuszynski/bch5884jek/blob/master/assignments/project_2/sec_peak_finder.py

#importing all required modules
import sys
import numpy as np
from scipy.signal import peak_widths, find_peaks
from matplotlib import pyplot as plt

time=[]
sig=[]
tpeaks=[]

def find_local_minima(arr,thr=5,noise=.1,target=tpeaks):
	for t in range(len(arr)):
		try:
			prev_min = arr[t-int(thr):t].min()
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

#translate values from minima points to real signal points
def match_sigs(arr, minima=tpeaks, ref=sig):
	for x in range(len(minima)):
		if np.isnan(minima[x]):
			arr.append(np.nan)
			continue
		else:
			arr.append(ref[x])

#open and parse the given file
f=open("superose6_50.asc")
lines=f.readlines()
f.close()

for line in lines[3:]:
	words=line.split()
	try:
		time.append(float(words[0]))
		sig.append(float(words[1]))
	except:
		continue

#setup x values from parsed file function
time=np.array(time)
sig=np.array(sig)
dsig=np.gradient(sig)
ddsig=np.gradient(dsig)

#find local minima from 2nd derivative
find_local_minima(ddsig,20,.5)

#use local minima to find corresponding values in original signal
peak_list=[]
match_sigs(peak_list)

p_widths=np.empty(881)

#find peak widths by checking 1st derivative until value less than/greater than changes from pos -> neg or opposite
def find_peak_widths(arr, dx=dsig, ref=sig):
	for i in range(len(peak_list)):
		if not np.isnan(peak_list[i]):
			for j in range(len(dx)):
				try:
					if dx[i+j] <= dx[i]:
						arr[i+j]=np.nan
					else:
						arr[i+j]=ref[i+j]
						break
				except IndexError:
					continue
		else:
			continue

#convert all 0's into nan values for matplotlib
find_peak_widths(p_widths)
p_widths=p_widths.tolist()
p_widths2=[np.nan if x==0 else x for x in p_widths]

#plot desired graph with peaks and widths
plt.plot(time,peak_list,'o')
plt.plot(time,p_widths2,'ro')
plt.plot(time,sig)
plt.xlim(0,164)
plt.ylim(15,1100)
plt.figure(figsize=(10,10))
plt.show()