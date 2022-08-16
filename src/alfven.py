# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 13:33:47 2021

@author: me
"""
import numpy as np

data = np.genfromtxt('C:/Users\me\Downloads\omni_min_MPLB_5zCad.lst')
doy = data[:,1]
data = data[:,5]
data[data == 999.9] = np.nan

indices = [i for i, x in enumerate(data) if x < 1.0]
daylist = []

for item in indices:
    daylist.append(doy[item])
    
daylist = np.array(daylist)