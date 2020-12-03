#!/usr/bin/env python3

import sys
import os
import re
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.colors as colors
import matplotlib.lines as lines
import seaborn as sns
from scipy import signal,optimize 

path="/mnt/c/Users/roflc/Desktop/MCD 11-11-20/"
d={}
df_avgs={}
df_diff={}

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

def plot_mcd(dic,op='avg',x_axis='Energy (eV)'):
    fig,ax=plt.subplots()
    # norm=plt.Normalize(-10,10) #optional to remove discrete H bar divisions
    norm=colors.BoundaryNorm(np.linspace(-10,10,11),ncolors=256)
    sm=plt.cm.ScalarMappable(cmap='coolwarm_r',norm=norm) 
    fig.colorbar(sm,ticks=range(-10,11,2),label='H (T)') #make color bar based on H (T) for plot
    for df in dic.values():
        #Dr. Seaborn or: How I Learned to Stop Worrying and Love sns.lineplot. Such efficiency. Much wow.
        sns.lineplot(data=df,x='energy',y='mdeg', linewidth=0.6,
                    hue='field',hue_norm=(-10,10),
                    palette=sns.color_palette('coolwarm_r',as_cmap=True),
                    legend=None)
    if x_axis=='Energy (eV)':
        plt.xlabel(x_axis)
    if op=='raw':
        plt.title("Raw MCD")
    if op=='avg':
        plt.title("Averaged MCD")
    plt.ylabel('MCD (mdeg)')
    plt.xlim(1.55,.75)
    plt.style.use('seaborn-paper')
    plt.savefig(op + '_mcd',dpi=300,transparent=True,bbox_inches='tight')
    plt.show()

def calc_raw_avg_mcd(dic): #need to define this before finding the mcd difference
    for name, df in dic.items():
        field = re.search('(.*)(?=T)',name).group(0) #set variable 'field' equal to int(field) from original dictionary
        if field not in df_avgs: 
            df_avgs[field] = pd.DataFrame() #if field is not in new dictionary, create an empty dataframe
        if field in df_avgs:
            df_concat=pd.concat([df_avgs[field], df]).groupby(['wavelength'], as_index=False) #concatenate field entry with new df entry, so long as field is matching
            df_avgs[field] = df_concat #update dictionary entry with newly concatenated one
        df_avgs[field]=df_avgs[field].mean() #take the average of the concatenated df

def calc_diff_mcd(dic,op='sub'):
    for name, df in dic.items():
        df_diff[name] = pd.DataFrame()
        if name == '0': 
            # if op=='add':
            #     df_diff[name] = df + dic[list(name)[list(name).index(name)+3]]
            # elif op=='sub':
            #     df_diff[name] = df - dic[list(name)[list(name).index(name)+3]]
            del df_diff[name] #placeholder for now. In future would like to plot 0T field difference, but previous function looks like it deletes a version of 0 so no pair to subtract.
            pass
        elif '-' not in name: #loop only positive half of dictionary
            if op=='add':
                df_diff[name] = df + dic['-' + name] #add positive and negative dictionary entries
                df_diff[name]['energy'] = df['energy'] #fix energy back to original values
                df_diff[name]['field'] = df['field'] #fix field back to original values
            elif op=='sub':
                df_diff[name] = df - dic['-' + name] #subtract positive and negative dictionary entries
                df_diff[name]['energy'] = df['energy'] #fix field back to original values
                df_diff[name]['field'] = df['field']
        else:
            del df_diff[name]
            continue
             
def plot_diff_mcd(dic,op='avg',x_axis='Energy (eV)'):
    fig,ax=plt.subplots()
    # norm=plt.Normalize(-10,10) #optional to remove discrete H bar divisions
    norm=colors.BoundaryNorm(np.linspace(0,10,6),ncolors=256)
    sm=plt.cm.ScalarMappable(cmap='Greys',norm=norm) 
    fig.colorbar(sm,ticks=range(0,11,2),label='H (T)') #make color bar based on H (T) for plot
    for name, df in dic.items():
        #Dr. Seaborn or: How I Learned to Stop Worrying and Love sns.lineplot. Such efficiency. Much wow.
        sns.lineplot(data=df,x='energy',y='mdeg', linewidth=0.6,
                    hue='field',hue_norm=(0,10),
                    palette=sns.color_palette('Greys',as_cmap=True),
                    legend=None)
    if x_axis=='Energy (eV)':
        plt.xlabel(x_axis)
    if op=='raw':
        plt.title("Raw MCD")
    if op=='avg':
        plt.title("Difference MCD")
    plt.ylabel('MCD (mdeg)')
    plt.xlim(1.55,.75)
    baseline = lines.Line2D(range(6),np.zeros(1),c='black')
    ax.add_line(baseline)
    plt.style.use('seaborn-paper')
    plt.savefig('diff_mcd',dpi=300,transparent=True,bbox_inches='tight')
    plt.show()

# def load_abs():

plot_mcd(d,'raw')
calc_raw_avg_mcd(d)
plot_mcd(df_avgs,'avg')
calc_diff_mcd(df_avgs)
plot_diff_mcd(df_diff)