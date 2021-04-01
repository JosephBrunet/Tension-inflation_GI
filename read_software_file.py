# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 19:50:39 2020

@author: WhoAreYou
"""



import numpy as np
import matplotlib.pyplot as plt
import pandas as pd   #  Pour manipuler des tableaux (comme dans excel)

import sys
import os


from tkinter import Tk 
from tkinter.filedialog import askopenfilename





def read():
    
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    print(filename)
    
    with open(filename) as f:
        txt = list(f)
        txt = txt[2:]
        
    
    txt_modif = []
    for i in range(0,len(txt)):
        if not (txt[i].find("Pause") != -1 or txt[i] == '\n'):
            txt_modif.append(txt[i])
        
    data = txt_modif
    t, d, F, P = [], [], [], []
    for i in range(1,len(data)):
        t.append(float(data[i].split(' , ')[0]))
        d.append(float(data[i].split(' , ')[1]))
        F.append(float(data[i].split(' , ')[2]))
        P.append(float(data[i].split(' , ')[3]))
    t, d, F, P = np.array(t), np.array(d), np.array(F), np.array(P)
    
    

    return t, d, F, P
    

def plot(x,y):
    # Data for plotting
    fig, ax = plt.subplots()
    
    ax.plot(x,y, 'k',alpha=0.9, linewidth = 1.8)
    #ax.plot(x,y, '+k',alpha=0.9)
    # p1, caplines1, barlinecols1 =  ax.errorbar(
    #     P, DintMean, [DintSTD, np.zeros(len(DintMean))], linestyle='None', ecolor='k', 
    #     marker='s', markerfacecolor='lightgrey', markersize=8, markeredgecolor='k')
    
 
    #plt.ylabel('Cauchy stress (kPa)',fontsize=14)
    #plt.xlabel('Stretch',fontsize=14)
    #plt.xticks(fontsize=14)
    #plt.yticks(fontsize=14)
    #plt.legend((p1, p2), ('Intimal side', 'Adventitial side'),loc=2, fontsize=14)
    plt.xlim(left=1) #xmin is your value
    #plt.xlim(right=xmax) #xmax is your value
    plt.ylim(bottom=0) #ymin is your value
    #plt.ylim(top=1750) #ymax is your value
    plt.ylabel('Nominal stress [kPa]',fontsize=14)
    plt.xlabel('Stretch',fontsize=14)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    # Only show ticks on the left and bottom spines
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    
    
    plt.savefig('plot_notch_long.pdf',bbox_inches='tight')
    plt.show()









def main():
    print("Hello world.")





if __name__ == "__main__":
    
    sys.exit()
    
    
    t, d, F, P = read()
    
    L0 = 14
    width = 7.5
    thickness = 2.44-1.21
    S=width*thickness

    lam = []
    cauchy = []
    for i in range(0,len(d)):
        lam.append((d[i]+L0)/L0)
        cauchy.append(1000*F[i]/S)
        
    #N1=2750
    N1 = 2460
    N2 = 3141
            
    plot(lam[N1:N2],cauchy[N1:N2]-cauchy[N1])
    #plot(lam[N1:],cauchy[N1:]-cauchy[N1])

        
    
    
    
    
    
    
    