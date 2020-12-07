#!/usr/bin/env python3

import sys
import os
import re
import pandas as pd
import numpy as np
import numpy.polynomial.polynomial as poly 
from matplotlib import pyplot as plt
import matplotlib.colors as colors
import matplotlib.lines as lines
import seaborn as sns
from scipy import signal,optimize,interpolate
import math

d={}
d_abs={}
df_avgs={}
df_diff={}

def parse_mcd(path):
    for root, dirs, files in os.walk(path): #walk along all files in directory given a path
        for num, name in enumerate(files): #for each file in list of files...
            if "test" not in str.lower(name): #remove any test files performed during data acqusition
                field_name = re.search('(.*)(?=T_)..',name).group(0) #search for beginning of file name "#T_" and set as name for df. Man this was difficult to figure out syntactically. 
                f=field_name + str(num%3) #differentiate repeated scans at same field
                # print("Adding", f + "...") #uncomment to check files are being added/named correctly
                df=pd.read_table(path+name, sep='\t',names=['wavelength','pemx','pemy','chpx','chpy','deltaA']) #create dataframe for each file
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

def parse_abs(path):
    for root, dirs, files in os.walk(path): #walk along all files in directory given a path
        for num, name in enumerate(files): #for each file in list of files...
            if "blank" or "ems" in str.lower(name): #remove any test files performed during data acqusition
                f = re.search('.*(?=_A)',name).group(0) #search for beginning of file name "#T_" and set as name for df. Man this was difficult to figure out syntactically. 
                # print("Adding", f + "...") #uncomment to check files are being added/named correctly
                df=pd.read_table(path+name, sep='\t',names=['wavelength','pemx','pemy','chpx','chpy','deltaA']) #create dataframe for each file
                df['energy']=1240/df['wavelength'] #calculate energy from wavelength
                d_abs[f] = df #send dataframe to dictionary
    df_abs=pd.DataFrame(data=(d_abs['Ems']['wavelength'], d_abs['Ems']['energy'], d_abs['Ems']['chpx'], d_abs['Blank']['chpx'])).transpose() #make dataframe from ems/blank dictionary
    df_abs.columns=['wavelength','energy','ems','blank'] #setup columns
    df_abs['absorbance']=(2-np.log10(100 * df_abs['ems'] / df_abs['blank'])) #calculate absorbance from emission and blank data
    df_abs['smoothed_absorbance']=signal.savgol_filter(df_abs['absorbance'],25,2) #smooth absorbance plot using Savitzky-Golay
    return df_abs

def plot_abs(df,op='smooth',x_axis='energy'):
    fig,ax=plt.subplots()
    if x_axis=='energy':
        plt.xlabel('Energy (eV)')
    if op=='raw':
        plt.title("Raw Absorbance")
        sns.lineplot(data=df,x='energy',y='absorbance', linewidth=0.6)
    if op=='smooth':
        plt.title("Smoothed Absorbance")
        sns.lineplot(data=df,x='energy',y='smoothed_absorbance', linewidth=0.6)
    plt.ylabel('Absorbance (a.u.)')
    plt.xlim(2.1,0.75)
    plt.style.use('seaborn-paper')
    plt.savefig(op + '_abs',dpi=300,transparent=True,bbox_inches='tight')
    plt.show()

def plot_CP_diff(x,y,ev=0.04):
    coeff_L=poly.polyfit([x+ev for x in x],y,9)
    coeff_R=poly.polyfit([x-ev for x in x],y,9)
    fit_L=poly.polyval(x,coeff_L)
    fit_R=poly.polyval(x,coeff_R)
    fit_diff=(fit_L-fit_R)/(np.max(x))*1000 #calculate LCP-RCP normalized to absorbance max. Will incorporate based on field later.
    # x = x.values.tolist()
    plt.figure(figsize=(6,6),dpi=80)

    plt.subplot(2,1,1)
    plt.ylabel('Absorbance (a.u.)')
    plt.xlim(2.1,0.55)
    plt.scatter(x,y,s=1.3,c='Black')
    plt.plot(x,fit_L,c='Blue')
    plt.plot(x,fit_R,c='Red')
    plt.legend(('LCP','RCP','Raw'))

    plt.subplot(2,1,2)
    plt.ylabel('Absorbance (a.u.)')
    plt.xlabel('Energy (eV)')
    plt.xlim(2.1,0.55)
    plt.plot(x,fit_diff,c='Purple')
    plt.legend(('Simulated MCD'))
    plt.show()

    return fit_diff

# df_abs['energy'],df_abs['absorbance']

def func(x,ev): #define simulated mcd function from absorbance spectrum
    coeff=poly.polyfit(df_abs['energy'],df_abs['absorbance'],9) #find polynomial coeffs from original absorption spectra
    LCP=poly.polyval(x+ev,coeff) #find y from +ev shifted LCP spectrum
    RCP=poly.polyval(x-ev,coeff) #find y from -ev shifted RCP spectrum
    return LCP-RCP #return y from LCP-RCP

    # coeff_L=poly.polyfit(x+ev,y,9)
    # coeff_R=poly.polyfit(x-ev,y,9)
    # coeff_fit=(coeff_L-coeff_R)
    # return coeff_fit

# def func(x,*p):
#     polyL = 0
#     polyR = 0
#     for i, n in enumerate(range(1:10)):
#         polyL += n * (x+ev)**i
#     for i, n in enumerate(range(1:10)):
#         polyR += n * (x-eV)**i
#     return poly

# def func(x,ev,*p):
#     x -= ev
#     poly.polyfit(x,y,9)
#     return 

def calc_effective_mass(abs_fit,diff_dic):
    ev_list=[]
    m_list=[]
    for field in diff_dic.keys():
        xdata=diff_dic[field]['energy'] 
        ydata=diff_dic[field]['mdeg']
        popt,pcov = optimize.curve_fit(func,xdata,ydata,bounds=(0,1)) #lsf optimization to spit out ev

        ev=popt[0] #return minimzed ev to variable
        ev_list.append(ev) #add ev to list
        c=299792458 #speed of light (m/s)
        e=1.60217662E-19 #charge of electron (C)
        m_e=9.10938356E-31 #mass of electron (kg)
        w_c=c/(1240/(ev/1000)*(10**-9)) #cyclotron resonance frequency
        effective_mass=e*int(field)/w_c/2/m_e/math.pi #effective mass (m*/m_e)
        m_list.append(effective_mass) #add m* to list

        plt.figure(figsize=(6,6),dpi=80)
        plt.title(str(field) + 'T Fit')
        plt.ylabel('MCD (deltaA/A_max*B) (T^-1) (x 10^-3)')
        plt.xlabel('Energy (eV)')
        plt.xlim(1.55,0.75)
        plt.plot(xdata,ydata,label='data')
        plt.plot(xdata,[func(x,*popt) for x in xdata],label='fit')
        plt.legend()
        plt.savefig(str(field) + "T_fit",dpi=300,transparent=True,bbox_inches='tight')
    print(ev_list)
    print(m_list)
        # simulated_fit=abs_fit/int(field) #normalized simulated fit by field
        # exp_coeff=poly.polyfit(x,y,9)*1000
        # experiment_fit=poly.polyval(x,exp_coeff)
        # experiment_fit=experiment_fit/np.max(np.absolute(experiment_fit)) #normalize experimental fit


        
        
        # plt.plot(x,experiment_fit,c='Black')
        # plt.plot(df_abs['energy'],simulated_fit,c='Red')
        # plt.legend(('Experimental MCD','Simulated MCD'))
        # plt.show()


# def modeleq(x,t):
# 	return x[0]+x[1]*np.exp(x[2]*t)
# def residuals(coeffs,t,y):
# # 	return modeleq(coeffs,t)-y
	
# def residuals(p,x,y):
#     return y-f(*p)

# popt, pcov = optimize.curve_fit()
# # print(popt)
# def data_calc():
#     x=df_abs['energy']
#     y=df_abs['absorbance']
#     x0=[1.0,1.0,1.0]
#     popt,pcov=optimize.least_squares(residuals,x0,args=(x,y))
#     print(popt)



# a=0.5
# b=2.0
# c=-1

# t_min=0
# t_max=10
# n_points=100

# t_train=np.linspace(t_min,t_max,n_points)
# y_train=gen_data(t_train,a,b,c,noise=0.1,n_outliers=10)

# x0 = np.array([1.0, 1.0, 0.0])
# res_lsq=leastsq(residuals, x0, args=(t_train,y_train))
# print (res_lsq)

# t_test= np.linspace(t_min,t_max,n_points*10)
# y_true= gen_data(t_test, a,b,c)
# y_lsq= gen_data(t_test, *res_lsq[0])
# resid=y_train-gen_data(t_train, *res_lsq[0])

# plt.plot(t_train,y_train,'o')
# plt.plot(t_test, y_true, 'k', linewidth=2, label='true')
# plt.plot(t_test,y_lsq, label='fitted')
# plt.plot(t_train, resid,'ro')
# plt.xlabel('t')
# plt.ylabel('y')
# plt.show()

parse_mcd("/mnt/c/Users/roflc/Desktop/MCD 11-11-20/")
df_abs = parse_abs("/mnt/c/Users/roflc/Desktop/Abs 11-11-20/")
plot_mcd(d,'raw')
calc_raw_avg_mcd(d)
plot_mcd(df_avgs,'avg')
calc_diff_mcd(df_avgs)
plot_diff_mcd(df_diff)
plot_abs(df_abs)
fit_diff=plot_CP_diff(df_abs['energy'],df_abs['absorbance'])
calc_effective_mass(fit_diff,df_diff)
