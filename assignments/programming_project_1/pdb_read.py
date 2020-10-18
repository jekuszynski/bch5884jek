#!/usr/bin/env python3

#import necessary modules
import sys

#open file for reading
pdb=open("2FA9noend.pdb",'r') 
all_rows=pdb.readlines()

# making empty lists for inputting info later
atom_list=[]
atom_type=[]
x_list=[]
y_list=[]
z_list=[]

#separate coordinate data from original file into x, y, z components & obtain elemental symbols as "type"
for row in all_rows:
    atom=row.split()
    atom_list.append(atom) #create list of atoms
    x=float(atom[6])
    y=float(atom[7])
    z=float(atom[8])
    atom_name=atom[11]
    x_list.append(x)
    y_list.append(y) 
    z_list.append(z)
    atom_type.append(atom_name)

#calculate total mass of system, tmass
mass_list=[]
tmass=0
for ele in atom_type:
    if ele is 'N':
        atom_mass = 14.01
        mass_list.append(atom_mass)
    if ele is 'C':
        atom_mass = 12.01
        mass_list.append(atom_mass)
    if ele is 'O':
        atom_mass = 16.00
        mass_list.append(atom_mass)
    if ele is 'S':
        atom_mass = 32.07
        mass_list.append(atom_mass)
    tmass+=atom_mass

#calculate the default center of mass along x, y, and z
cmx_default=0
cmy_default=0
cmz_default=0
for m in range(len(atom_type)):
    cmx_default+=(mass_list[m]*x_list[m]/tmass)
    cmy_default+=(mass_list[m]*y_list[m]/tmass)
    cmz_default+=(mass_list[m]*z_list[m]/tmass)

#input new center of mass from user
cmx=int(input("Please input desired center of mass x coordinate: "))
cmy=int(input("Please input desired center of mass y coordinate: "))
cmz=int(input("Please input desired center of mass z coordinate: "))

#calculate difference between default and input CoM
xshift=cmx-cmx_default
yshift=cmy-cmy_default
zshift=cmz-cmz_default

#calculate shift in coordinates
x_new=[]
y_new=[]
z_new=[]
mx=0
my=0
mz=0
for m in range(len(atom_type)):
    x=round(x_list[m]+xshift,3)
    x_new.append(x)
    y=round(y_list[m]+yshift,3)
    y_new.append(y)
    z=round(z_list[m]+zshift,3)
    z_new.append(z)

#make changes to coordinates based on previously calculated shift    
for row in range(len(atom_list)):
    atom_list[row][6] = x_new[row]
    atom_list[row][7] = y_new[row]
    atom_list[row][8] = z_new[row]

#write file out
pdb_new = open("new.pdb","w") 
for row in atom_list:
    for col in row:
        f='{0:%-6s%5d%-4s%1s%3d%1s%8.3f%8.3f%8.3f%6.2f%6.2f%2.2s%2.2s}\n'
        pdb_new.write(f.format(str(col)))
pdb_new.close()

sys.exit()

pdb_new = open("new.pdb","w") 
for row in atom_list:
    for col in row:
        pdb_new.write(str(col))
    pdb_new.write('\n')
pdb.format('%-6s%5d%-4s%1s%3d%1s%8.3f%8.3f%8.3f%6.2f%6.2f%2.2s%2.2s')
pdb_new.close()
#pdb_new.write('%-6s%5d%-4s%1s%3d%1s%8.3f%8.3f%8.3f%6.2f%6.2f%2.2s%2.2s' % str(row[1])


#"%-6s%5d%-4s%1s%3d%1s%8.3f%8.3f%8.3f%6.2f%6.2f%2.2s%2.2s\n"

#.format('%-6s%5d%-4s%1s%3d%1s%8.3f%8.3f%8.3f%6.2f%6.2f%2.2s%2.2s\n')
#f=open("tmp.out",'w') #open file for writing
#for temp in tmplist:
# s="The temperature factor is {0:6.3f}\n" #\n for including data in separate lines\
#f.write(s.format((temp))
