import matplotlib.pyplot as plt
from spacepy.pybats import bats
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import numpy as np
from spacepy.plot import style
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from matplotlib.lines import Line2D

def mhd(filename):
    LT = int(filename[-11:-9])
    mag = bats.MagFile(filename)
    t = mag['time']
    mhd = np.zeros(shape = (1, 15, 8101))

    #convert MHD vectors to SM coordinates
    mhd[0] = np.array([mag['d10']['dBnMhd'], mag['d15']['dBnMhd'], mag['d20']['dBnMhd'], 
                       mag['d25']['dBnMhd'], mag['d30']['dBnMhd'], mag['d35']['dBnMhd'], 
                       mag['d40']['dBnMhd'], mag['d45']['dBnMhd'], mag['d50']['dBnMhd'], 
                       mag['d55']['dBnMhd'], mag['d60']['dBnMhd'], mag['d65']['dBnMhd'], 
                       mag['d70']['dBnMhd'], mag['d75']['dBnMhd'], mag['d80']['dBnMhd']])
    
    return t, mhd

LT00 = mhd('MHD/LT_00_mags.mag')
LT03 = mhd('MHD/LT_03_mags.mag')
LT06 = mhd('MHD/LT_06_mags.mag')
LT09 = mhd('MHD/LT_09_mags.mag')
LT12 = mhd('MHD/LT_12_mags.mag')
LT15 = mhd('MHD/LT_15_mags.mag')
LT18 = mhd('MHD/LT_18_mags.mag')
LT21 = mhd('MHD/LT_21_mags.mag')

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
for num, item in enumerate(LT00[1][0]):
    #ax.plot(LT00[0], LT00[1][0][num], color = 'red')
    #ax.plot(LT03[0], LT03[1][0][num], color = 'orange')
    #ax.plot(LT06[0], LT06[1][0][num], color = 'yellow')
    #ax.plot(LT09[0], LT09[1][0][num], color = 'green')
    ax.plot(LT12[0], LT12[1][0][num], color = 'blue')
    #ax.plot(LT15[0], LT15[1][0][num], color = 'indigo')
    #ax.plot(LT18[0], LT18[1][0][num], color = 'purple')
    #ax.plot(LT21[0], LT21[1][0][num], color = 'gray')

    
box = plt.gca().get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(custom_lines, ['LT00', 'LT03', 'LT06', 'LT09', 'LT12', 'LT15', 'LT18', 'LT21'], loc='center left', bbox_to_anchor=(1, 0.5), frameon = True)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.ylim(-250, 320)
plt.xlim((datetime(2015, 3, 21, 5, 58, 20), datetime(2015, 3, 21, 6, 8, 11)))
#plt.title(f"{frame.hour:02}"+':'+f"{frame.minute:02}"+':'+f"{frame.hour:02}")
plt.ylabel(r'$B_z \ (nT)$')
plt.xlabel('UT (HH:MM)')
plt.tick_params(rotation=45)