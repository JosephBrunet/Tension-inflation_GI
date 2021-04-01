#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 16:58:25 2019

@author: joseph.brunet
"""




import numpy as np
from scipy import optimize
from scipy.signal import argrelextrema
from scipy.interpolate import interp1d
import pandas as pd
import matplotlib.pyplot as plt 
import math

from tkinter import Tk
from tkinter.filedialog import askopenfilename

import datetime





#------------------------------------------------------------
## FILE NAME
#------------------------------------------------------------

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(filename)



file_name=filename

#file_name = '/media/utilisateur/Jo/System_tomo/Code test/Working_dir/ech1_15.txt'
##file_name = '/media/utilisateur/Jo/System_tomo/Code test/test.txt'
#file_name = '/media/joseph.brunet/Jo/System_tomo/Code test/test.txt'



#------------------------------------------------------------
## CONSTANTES
#------------------------------------------------------------

L0=21
#Di=3
#De=3.5

#S = (math.pi * (De/2)**2) - (math.pi * (Di/2)**2)




#------------------------------------------------------------
## READ FILE
#------------------------------------------------------------

file = open(file_name, 'r') 
txt = file.readlines() 

save_file = pd.Series(txt)
save_file = save_file.replace(r'\n','', regex=True) 


save_file = save_file.replace('',np.NaN, regex=True) 
save_file = save_file.dropna()

print("File name: "+save_file[0] )


pause = []
unpause = []
scan = []
save = 0
t = []
d = []
F = []
P = []
V = []

for i in save_file[4:len(save_file)]:
    
    if i == 'Pause':
        pause.append(save)
        
    elif i == 'End Pause':
        unpause.append(save)   
        
    elif i.find("Scan start") != -1:
        scan.append(save)
    
    
    else:
        t.append(float(i.split(' , ')[0]))
        d.append(float(i.split(' , ')[1]))
        F.append(float(i.split(' , ')[2]))
        P.append(float(i.split(' , ')[3]))
        V.append(float(i.split(' , ')[4]))
        
        save = float(i.split(' , ')[0])
    




#    
#lambda = [1+ i/L0 for i in d]
#nominalS = [i/S for i in F]


d = np.asarray(d)
F = np.asarray(F)
t = np.asarray(t)








#------------------------------------------------------------
## SEARCH LOCAL MINIMA
#------------------------------------------------------------


## for local minima
#min_index = argrelextrema(d, np.less_equal,order=2)[0]
## for local maxima
#max_index = argrelextrema(d, np.greater_equal,order=2)[0]
##d[argrelextrema(d, np.greater)[0]]
#
#for i in range(len(min_index)-1,0,-1):
#    if min_index[i-1] == min_index[i]-1:
#        min_index = np.concatenate((min_index[0:i], min_index[i+1:]))
#for i in range(len(max_index)-1,0,-1):
#    if max_index[i-1] == max_index[i]-1:
#        max_index = np.concatenate((max_index[0:i], max_index[i+1:]))


#d = d[min_index[2]:max_index[-1]]
#F = F[min_index[2]:max_index[-1]]

#------------------------------------------------------------
## PLOT
#------------------------------------------------------------
 


# plotting points as a scatter plot 
plt.scatter(t, P, label= "stars", color= "green",  marker= "*", s=30)
plt.scatter(t, F, label= "stars", color= "green",  marker= "*", s=30)

for i in pause:
    plt.axvline(x=i, color='r', linestyle='--')
for i in unpause:
    plt.axvline(x=i, color='k', linestyle='--')
#plt.scatter(t[min_index, d[min_index])
#plt.scatter(t[max_index], d[max_index])
# x-axis label 
plt.xlabel('t') 
# frequency label 
plt.ylabel('d') 
# plot title 
plt.title('My scatter plot!') 
# showing legend 
plt.legend()   
plt.show() 





plt.figure()
plt.scatter(t, F, label= "stars", color= "green",  marker= "*", s=30)
plt.show() 



##------------------------------------------------------------
## FIND MEAN 
#------------------------------------------------------------

line = save_file[1:2].values[0].split(' ')[-1].split(":")
h = line[0]
m =line[1]
s = line[2]
time_acqui = float(h)*60*60 + float(m)*60 + float(s)

time_2_remove = float(save_file[len(save_file)-1].split(' ')[0])
time_acqui_real = time_acqui - time_2_remove

line=save_file[2:3].values[0].split(' ')[-1].split(":")
h = line[0]
m =line[1]
s = line[2]
time_scan = float(h)*60*60 + float(m)*60 + float(s)

time_waiting = time_scan - time_acqui_real

tt=[]
PP=[]
FF=[]
for k in range(0,len(t)):
    if t[k]> time_waiting and t[k] < time_waiting+266:
        tt.append(t[k])
        PP.append(P[k])
        FF.append(F[k])

plt.figure()    
plt.scatter(t, P, label= "stars", color= "green",  marker= "*", s=30)
plt.axvline(x=time_waiting, color='r', linestyle='--')
plt.axvline(x=time_waiting+266, color='k', linestyle='--')
    
plt.figure()
plt.scatter(t, F, label= "stars", color= "green",  marker= "*", s=30)
plt.axvline(x=time_waiting, color='r', linestyle='--')
plt.axvline(x=time_waiting+266, color='k', linestyle='--')



np.mean(PP)
np.mean(FF)


#10    1.7
#80    2.2
#130   2.2
#315   1.0
#500   1.1
#700   0.5
#950   0.0

path_img = '/media/joseph.brunet/Jo/Tomo/06_12_2019/Ech1/tiff/'

pressure = ['10', '80', '130','315','500','700','950']
pres = [10,59,103,301,436,590,687]

F_mean = [1.7, 2.2, 2.2, 1.0, 1.1, 0.5, 0.0]



fig, ax1 = plt.subplots()
ax1.set_xlabel('Pressure (mmHg)', fontsize=12)
ax1.set_ylabel('Mean axial load (N)', fontsize=12)
ax1.plot(pres,F_mean, color='k',linewidth=1.0)


ax1.scatter(pres,F_mean, marker='s',color='k', label='Volume ')


plt.savefig(path_img+'graph_axial_load.pdf',bbox_inches='tight')
plt.show() 




##------------------------------------------------------------
## SMOOTHING
#------------------------------------------------------------

#
#f = interp1d(d, F)
#f2 = interp1d(d, F, kind='cubic')
#
#
#
#
#fig, axs = plt.subplots(3, figsize=(10,15))
#fig.suptitle('Vertically stacked subplots')
#axs[0].plot(d, F, 'o')
#axs[1].plot(d, f(d), '-')
#axs[2].plot(d, f2(d), '--')
#plt.show()
#
#
#from scipy.signal import savgol_filter
#
#savgol_filter(x, 5, 2)
#





#
#x = np.linspace(0,2*np.pi,100)
#y = np.sin(x) + np.random.random(100) * 0.2
#yhat = savgol_filter(F, 51, 3) # window size 51, polynomial order 3
#
#plt.figure(figsize=(10,10))
#plt.plot(d,F)
#plt.plot(d,yhat, color='red')
#plt.legend(['Experiment','Smoothing'],prop={'size': 20})
#plt.show()



##------------------------------------------------------------
## FITTING
#------------------------------------------------------------
 



#def test_func(x, a, b):
#    return a * x + b
#
#params, params_covariance = optimize.curve_fit(test_func, d, F,p0=[2, 2])
#
#print(params)
#
#
#
#
#plt.scatter(d, F, label='Data')
#plt.plot(d, test_func(d, params[0], params[1]),label='Fitted function')
#
#plt.legend(loc='best')
#
#plt.show()






















