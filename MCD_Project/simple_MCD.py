#!/usr/bin/env python3

import sys
import os
from glob import glob
import re
import pandas as pd
import numpy as np
from scipy import signal,optimize 
from matplotlib import pyplot as plt
import matplotlib.cm as mplcm
import matplotlib.colors as colors
import seaborn

path="/mnt/c/Users/roflc/Desktop/MCD 11-11-20/"
d={}

for root, dirs, files in os.walk(path): #walk along all files in directory given a path
    for num, fname in enumerate(files): #for each file in list of files...
        if "test" not in str.lower(fname): #remove any test files performed during data acqusition
            field = re.search('(.*)(?=T_)..',fname).group(0) #search for beginning of file name "#T_" and set as name for df. Man this was difficult to figure out syntactically. 
            f=field + str(num%3) #differentiate repeated scans at same field
            # print("Adding", f + "...") #uncomment to check files are being added/named correctly
            df=pd.read_table(path+fname, sep='\t',names=['wavelength','chpx','chpy','pemx','pemy','deltaA']) #create dataframe for each file
            df['field']=int(re.search('(.*)(?=T)',fname).group(0)) #add column for field
            df['energy']=1240/df['wavelength'] #calculate energy from wavelength
            df['mdeg']=df['deltaA']*32982 # calculate mdeg from deltaA
            d[f] = df #send dataframe to dictionary

# print(d['-4T_0']['field'])
# sys.exit()

# fig = plt.figure()
# ax = fig.add_subplot(111)
cmap = plt.get_cmap('coolwarm') #set colormap for pos/neg field plotting
norm = colors.Normalize(vmin=-10,vmax=10) #normalize colormap knowing that only -10T and 10T are possible
fig,ax=plt.subplots()
for name, df in d.items():
    x=d[name]['energy']
    y=d[name]['mdeg']
    c=d[name]['field']
    ax.scatter(x,y,label=name,color=cmap(norm(c.values)))
    ax.legend(ncol=5)

sm=plt.cm.ScalarMappable(cmap=cmap,norm=norm)
fig.colorbar(sm)
plt.xlabel('Wavelength (nm)')
plt.ylabel('MCD (mdeg)')
plt.title("Raw MCD")
plt.xlim(1.55,.75)
plt.style.use('seaborn-paper')
plt.show()

