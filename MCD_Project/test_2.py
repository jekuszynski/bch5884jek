# #!/usr/bin/env python3

# import sys
# import os
# import glob
# import numpy as np
# import pandas as pd
# from scipy import signal,optimize 
# from matplotlib import pyplot as plt

# class MCD():
#     def __init__(self,folder):

#         path='/mnt/c/Users/roflc/Desktop/MCD 07-29-20/'

#         for file in glob.glob(os.path.join(path,folder)):    
#             pd.read_table(file,sep='\t')

#             name=[]
#             wavelength=[]
#             energy=[]
#             chopperx=[]
#             choppery=[]
#             pemx=[]
#             pemy=[]
#             da=[]
#             mdeg=[]

#             name.append(os.listdir(file))

#             for line in lines:
#                 col=line.split()
#                 wavelength.append(int(col[0]))
#                 chopperx.append(float(col[1]))
#                 choppery.append(float(col[2]))
#                 pemx.append(float(col[3]))
#                 pemy.append(float(col[4]))
#                 da.append(float(col[5]))
            
#             self.wavelength=np.array(wavelength)
#             self.chopperx=np.array(chopperx)
#             self.choppery=np.array(choppery)
#             self.pemx=np.array(pemx)
#             self.pemy=np.array(pemy)
#             self.da=np.array(da)
#             self.name=np.array(name)

#     def plot(self):
#         plt.plot(self.wavelength,self.da)
#         plt.show()

# if __name__ == "__main__":
#     mcd=MCD("Good")
#     print(MCD.da)
#     mcd.plot()

l={*range(-10,11,2)}
print(l)