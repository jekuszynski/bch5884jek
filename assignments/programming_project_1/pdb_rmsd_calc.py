#!/usr/bin/env python3
#https://github.com/jekuszynski/bch5884jek/blob/master/assignments/programming_project_1/pdb_rmsd_calc.py

import sys
from math import sqrt

def readpdb(filename):
    '''Parse pdb'''
    pdb=open(filename,'r')
    rows=pdb.readlines()
    pdb.close()
    '''Return data in dictioned, list form'''
    records=[]
    for data in rows:
        if data[:4]=="ATOM":
            d={}
            d['rtype']=data[0:6]
            d['atomnumber']=int(data[6:11])
            d['atomtype']=data[12:16]
            d['altloc']=data[16:17]
            d['residue']=data[17:20]
            d['chain']=data[21:22]
            d['residuenumber']=int(data[22:26])
            d['icode']=data[26:27]
            d['x']=float(data[30:38])
            d['y']=float(data[38:46])
            d['z']=float(data[46:54])
            d['occupancy']=float(data[54:60])
            d['tempfact']=float(data[60:66])
            d['element']=data[76:78].strip()
            d['charge']=data[78:80].strip()
            records.append(d)
    return records

def rmsd(file1,file2):
    '''Take two lists from pdb's and return RMSD'''
    rmsd_sum=0
    n=len(file1)
    for atom in range(len(file1)):
        xdiff=(file1[atom]['x']-file2[atom]['x'])**2
        ydiff=(file1[atom]['y']-file2[atom]['y'])**2
        zdiff=(file1[atom]['z']-file2[atom]['z'])**2
        rmsd_sum+=(xdiff+ydiff+zdiff)
    tot_rmsd=sqrt(rmsd_sum/n)
    return tot_rmsd

if __name__=="__main__":
    '''Perform RMSD calc using previously defined functions'''
    pdb1=readpdb("2FA9noend.pdb") 
    pdb2=readpdb("2FA9noend2mov.pdb")
    rmsd=rmsd(pdb1,pdb2)
    print ("The calculated RMSD for your two input pdb files is %.5f" % rmsd)