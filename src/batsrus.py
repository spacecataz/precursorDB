# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 12:20:53 2021

@author: me
"""
from spacepy.pybats import bats
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from spacepy.plot import style
import numpy as np
from matplotlib.lines import Line2D


def SM_convert(filename):
    LT = int(filename[-11:-9])
    maglat = 10
    x, y, z = [], [], []
    mag = bats.MagFile(filename)
    t = mag['time']
    plotlen = len(mag['time'])
    while maglat <= 80:
        for num, item in enumerate(mag['time']):
            x.append(-mag['d'+str(maglat)]['dBn'][num] * np.cos((np.pi/2)-(maglat * np.pi / 180)) * np.cos(LT * np.pi /12) - mag['d'+str(maglat)]['dBd'][num] * np.sin((np.pi/2)-(maglat * np.pi / 180)) * np.cos(LT * np.pi/12) - mag['d'+str(maglat)]['dBe'][num] * np.sin(LT*np.pi/12))
            y.append(-mag['d'+str(maglat)]['dBn'][num] * np.cos((np.pi/2)-(maglat * np.pi / 180)) * np.sin(LT * np.pi / 12) - mag['d'+str(maglat)]['dBd'][num] * np.sin((np.pi/2)-(maglat * np.pi / 180)) * np.sin(LT * np.pi/12) + mag['d'+str(maglat)]['dBe'][num] * np.cos(LT*np.pi/12))
            z.append(mag['d'+str(maglat)]['dBn'][num] * np.sin((np.pi/2)-(maglat * np.pi / 180)) - mag['d'+str(maglat)]['dBd'][num] * np.cos((np.pi/2)-(maglat * np.pi / 180)))
        maglat += 5
    x=np.array_split(x, len(x)/plotlen)
    y=np.array_split(y, len(y)/plotlen)
    z=np.array_split(z, len(z)/plotlen)
    return x, y, z, t, LT
    
LT00 = SM_convert('MHD/LT_00_mags.mag')
LT03 = SM_convert('MHD/LT_03_mags.mag')
LT06 = SM_convert('MHD/LT_06_mags.mag')
LT09 = SM_convert('MHD/LT_09_mags.mag')
LT12 = SM_convert('MHD/LT_12_mags.mag')
LT15 = SM_convert('MHD/LT_15_mags.mag')
LT18 = SM_convert('MHD/LT_18_mags.mag')
LT21 = SM_convert('MHD/LT_21_mags.mag')

custom_lines = [Line2D([0], [0], color='red', lw=1),
                Line2D([0], [0], color='orange', lw=1),
                Line2D([0], [0], color='yellow', lw=1),
                Line2D([0], [0], color='green', lw=1),
                Line2D([0], [0], color='blue', lw=1),
                Line2D([0], [0], color='indigo', lw=1),
                Line2D([0], [0], color='violet', lw=1),
                Line2D([0], [0], color='gray', lw=1)]

style()
fig, ax = plt.subplots()
for num, item in enumerate(LT00[2]):
    ax.plot(LT00[3], item - item[899], color = 'red')
    ax.plot(LT03[3], LT03[2][num] - LT03[2][num][899], color = 'orange')
    ax.plot(LT06[3], LT06[2][num] - LT06[2][num][899], color = 'yellow')
    ax.plot(LT09[3], LT09[2][num] - LT09[2][num][899], color = 'green')
    ax.plot(LT12[3], LT12[2][num] - LT12[2][num][899], color = 'blue')
    ax.plot(LT15[3], LT15[2][num] - LT15[2][num][899], color = 'indigo')
    ax.plot(LT18[3], LT18[2][num] - LT18[2][num][899], color = 'violet')
    ax.plot(LT21[3], LT21[2][num] - LT21[2][num][899], color = 'gray')
box = plt.gca().get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(custom_lines, ['LT00', 'LT03', 'LT06', 'LT09', 'LT12', 'LT15', 'LT18', 'LT21'], loc='center left', bbox_to_anchor=(1, 0.5), frameon = True)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.tick_params(rotation=45)
plt.title("All virtual mags, SM coordinate, z-direction")
plt.xlim((LT00[3][0],LT00[3][2000]))
plt.ylabel(r'$B_z \ (nT)$')
plt.xlabel("Time (MM:SS)")
plt.savefig('precursorDB/docs/EventList/SEA/ideal_ssc/SM/AllComponents.png')