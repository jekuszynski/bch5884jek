#!/usr/bin/env python3

import sys
import os
from glob import glob
import re
import pandas as pd
import numpy as np
from scipy import signal,optimize 
from matplotlib import pyplot as plt

path="/mnt/c/Users/roflc/Desktop/MCD 11-11-20/"
d={}

for root, dirs, files in os.walk(path): #walk along all files in directory given a path
    for num, fname in enumerate(files): #for each file in list of files...
        if "test" not in str.lower(fname): #remove any test files performed during data acqusition
            field = re.search('(.*)(?=T_)..', fname).group(0) #search for beginning of file name "#T_" and set as name for df. Man this was difficult to figure out syntactically. 
            f=field + str(num%3) #differentiate repeated scans at same field
            # print("Adding", f + "...") #check files are being added/named correctly
            d[f]=pd.read_table(path+fname, sep='\t',names=['wavelength','chpx','chpy','pemx','pemy','mcd']) #create dataframe for each file

# for name, df in d.items():
#     print(name)


