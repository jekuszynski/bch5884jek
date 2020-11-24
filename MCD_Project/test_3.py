#!/usr/bin/env python3

import sys
import os
import glob
import numpy as np
import pandas as pd
from scipy import signal,optimize 
from matplotlib import pyplot as plt

path='/mnt/c/Users/roflc/Desktop/MCD 07-29-20/Good'

for file in glob.glob(os.path.join(path)):    
    pd.read_table(file,sep='\t',header=None,names=[wavelength,chx,chy,pemx,pemy,da])

print