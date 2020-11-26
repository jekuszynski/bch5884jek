#!/usr/bin/env python3

import sys
import os
import re
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.colors as colors
import seaborn as sns
from scipy import signal,optimize 

path="/mnt/c/Users/roflc/Desktop/MCD 11-11-20/"
d={}
dd={}

for root, dirs, files in os.walk(path): #walk along all files in directory given a path
    for num, name in enumerate(files): #for each file in list of files...
        if "test" not in str.lower(name): #remove any test files performed during data acqusition
            field_name = re.search('(.*)(?=T_)..',name).group(0) #search for beginning of file name "#T_" and set as name for df. Man this was difficult to figure out syntactically. 
            f=field_name + str(num%3) #differentiate repeated scans at same field
            # print("Adding", f + "...") #uncomment to check files are being added/named correctly
            df=pd.read_table(path+name, sep='\t',names=['wavelength','chpx','chpy','pemx','pemy','deltaA']) #create dataframe for each file
            df['field']=int(re.search('(.*)(?=T)',name).group(0)) #add column for field
            df['energy']=1240/df['wavelength'] #calculate energy from wavelength
            df['mdeg']=df['deltaA']*32982 # calculate mdeg from deltaA
            d[f] = df #send dataframe to dictionary

# print(d['-4T_0']['field'])
# sys.exit()

# old code - keeping for posterity
    # fig = plt.figure()
    # ax = fig.add_subplot(111)

    # cmap = plt.get_cmap('coolwarm') #set colormap for pos/neg field plotting
    # norm = colors.Normalize(vmin=-10,vmax=10) #normalize colormap knowing that only -10T and 10T are possible
    # fig,ax=plt.subplots()
    # for name, df in d.items():
    #     x=d[name]['energy']
    #     y=d[name]['mdeg']
    #     c=d[name]['field']
    #     ax.scatter(x,y,label=name,color=cmap(norm(c.values)))
    #     ax.legend(ncol=5)

def plot_raw_mcd_eV(dic):
    fig,ax=plt.subplots()
    # norm=plt.Normalize(-10,10) #optional to remove discrete H bar divisions
    norm=colors.BoundaryNorm(np.linspace(-10,10,11),ncolors=256)
    sm=plt.cm.ScalarMappable(cmap='coolwarm_r',norm=norm)
    fig.colorbar(sm,ticks=range(-10,11,2),label='H (T)')

    for name, df in dic.items():
        #Dr. Seaborn or: How I Learned to Stop Worrying and Love sns.lineplot. Such efficiency. Wow.
        sns.lineplot(data=df,x='energy',y='mdeg', linewidth=0.6,
                    hue='field',hue_norm=(-10,10),
                    palette=sns.color_palette('coolwarm_r',as_cmap=True),
                    legend=None)

    plt.xlabel('Energy (eV)')
    plt.ylabel('MCD (mdeg)')
    plt.title("Raw MCD")
    plt.xlim(1.55,.75)
    plt.style.use('seaborn-paper')
    plt.show()

# def calc_raw_avg_mcd_eV(dic): #Need to define this before finding the mcd difference? 

#Could do both separately, but perhaps not good use of time. Maybe add separately later.



# def calc_diff_mcd_eV(dic): #think about adding an add/sub option hear. Look up in Notion notes.
#     for name, df in dic.items():
#         x=d[name]['energy']
#         c=d[name]['field']
#         if int(re.search('(.*)(?=T)',name).group(0)) > 0:
#             y=d[name]['mdeg']-d['-'+name]['mdeg'] #change to flip data. Will fix as option for function later.
#         elif int(re.search('(.*)(?=T)',name).group(0)) = 0:
#             y=d[name]['mdeg']-d[name]['mdeg']
#         else:
#             break

        
#         for ddname, dddf in dd.items():
#             if ddname == 

#         df = 
#         d[diff] =
#         return d[diff]


def plot_diff_mcd_eV(dic):
    fig,ax=plt.subplots()
    norm=colors.BoundaryNorm(np.linspace(-10,10,11),ncolors=256)
    sm=plt.cm.ScalarMappable(cmap='coolwarm_r',norm=norm)
    fig.colorbar(sm,ticks=range(-10,11,2),label='H (T)')

    for name, df in dic.items():
        #Dr. Seaborn or: How I Learned to Stop Worrying and Love sns.lineplot. Such efficiency. Wow.
        sns.lineplot(data=df,x='energy',y='mdeg', linewidth=0.6,
                    hue='field',hue_norm=(-10,10),
                    palette=sns.color_palette('coolwarm_r',as_cmap=True),
                    legend=None)

    plt.xlabel('Energy (eV)')
    plt.ylabel('MCD (mdeg)')
    plt.title("Difference MCD")
    plt.xlim(1.55,.75)
    plt.style.use('seaborn-paper')
    plt.show()

plot_raw_mcd_eV(d)
# plot_diff_mcd_eV(d)
