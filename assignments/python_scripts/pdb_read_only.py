#https://github.com/jekuszynski/bch5884jek/blob/master/assignments/python_scripts/pdb_read_only.py
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