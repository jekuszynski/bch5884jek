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
x_new=[]
y_new=[]
z_new=[]

#separate coordinate data from original file into x, y, z components & obtain elemental symbols as "type"
for row in all_rows:
    atom=row.split()
    #convert strings from original file into proper type
    atom[1] = int(atom[1])
    atom[5] = int(atom[5])
    atom[9] = float(atom[9])
    atom[10] = float(atom[10])
    #create list of atoms
    atom_list.append(atom) 
    x=float(atom[6])
    y=float(atom[7])
    z=float(atom[8])
    atom_name=atom[11]
    x_list.append(x)
    y_list.append(y) 
    z_list.append(z)
    atom_type.append(atom_name)

#calculate total mass of system
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

#Asks for data file change by GC or CM
choice=input("Please select Geometric Center [GC] or Center of Mass [CM]: ")

if choice.upper() == 'CM':
    #calculate the default center of mass along x, y, and z
    cmx_default=0
    cmy_default=0
    cmz_default=0
    for m in range(len(atom_type)):
        cmx_default+=(mass_list[m]*x_list[m]/tmass)
        cmy_default+=(mass_list[m]*y_list[m]/tmass)
        cmz_default+=(mass_list[m]*z_list[m]/tmass)

    #So I realized halfway through coding the CM part that you weren't asking for 
    #a USER input of center of mass, but rather just to find the CM and shift based on that...
    #But through this you can actually choose your own CM to shift all other atoms around the given
    #set of coordinates which is kind of cool? Otherwise not entering a value will give default
    #CM so... neat?

    #input new center of mass from user
    cmx=int(input("Please input desired center of mass x coordinate: ") or "0")
    cmy=int(input("Please input desired center of mass y coordinate: ") or "0")
    cmz=int(input("Please input desired center of mass z coordinate: ") or "0")

    #calculate difference between default and input CoM
    xshift=cmx-cmx_default
    yshift=cmy-cmy_default
    zshift=cmz-cmz_default

    #calculate shift in coordinates
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

elif choice.upper() == 'GC':
    #calculate total coordinate shifts
    for coord in range(len(atom_type)):
        x+=x_list[coord]
        y+=y_list[coord]
        z+=z_list[coord]

    #calculate mean coordinate shifts
    xshift = x/len(x_list)
    yshift = y/len(y_list)
    zshift = z/len(z_list) 

    #shift original coordinates to make new lists
    for g in range(len(atom_type)):
        x=round(x_list[g]+xshift,3)
        x_new.append(x)
        y=round(y_list[g]+yshift,3)
        y_new.append(y)
        z=round(z_list[g]+zshift,3)
        z_new.append(z)

else:
    print("Wrong Input! Please type GC or CM when prompted.")
    sys.exit()

#make changes to coordinates in originally created list based on calculated shifts   
for row in range(len(atom_list)):
    atom_list[row][6] = x_new[row]
    atom_list[row][7] = y_new[row]
    atom_list[row][8] = z_new[row]

#format file for writing
pdb_format='{:6s}{:5d} {:^4s}{:1s} {:3s} {:1d} {:8.3f}{:8.3f}{:8.3f}{:6.2f}{:6.2f} {:>2s}\n'

#generate new file and write
pdb_new = open("new.pdb","w") 
#flat_list=[item for elem in atom_list for item in elem]
for row in atom_list:
    pdb_new.write(pdb_format.format(*row))
pdb_new.close()
print("File successfully generated as 'new.pdb'!")

sys.exit()