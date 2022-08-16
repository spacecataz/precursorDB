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
    mhd = np.zeros(shape = (3, 13, 8101))

	#convert MHD vectors to SM coordinates
    mhd[0] = np.array([-mag['DST']['dBnMhd'] * np.cos((np.pi/2)-(10 * np.pi / 180)) * np.cos(LT * np.pi /12) - mag['DST']['dBdMhd'] * np.sin((np.pi/2)-(10 * np.pi / 180)) * np.cos(LT * np.pi/12) - mag['DST']['dBeMhd'] * np.sin(LT*np.pi/12),
                       -mag['YKC']['dBnMhd'] * np.cos((np.pi/2)-(15 * np.pi / 180)) * np.cos(LT * np.pi /12) - mag['YKC']['dBdMhd'] * np.sin((np.pi/2)-(15 * np.pi / 180)) * np.cos(LT * np.pi/12) - mag['YKC']['dBeMhd'] * np.sin(LT*np.pi/12),
                       -mag['MEA']['dBnMhd'] * np.cos((np.pi/2)-(20 * np.pi / 180)) * np.cos(LT * np.pi /12) - mag['MEA']['dBdMhd'] * np.sin((np.pi/2)-(20 * np.pi / 180)) * np.cos(LT * np.pi/12) - mag['MEA']['dBeMhd'] * np.sin(LT*np.pi/12),
                       -mag['NEW']['dBnMhd'] * np.cos((np.pi/2)-(25 * np.pi / 180)) * np.cos(LT * np.pi /12) - mag['NEW']['dBdMhd'] * np.sin((np.pi/2)-(25 * np.pi / 180)) * np.cos(LT * np.pi/12) - mag['NEW']['dBeMhd'] * np.sin(LT*np.pi/12),
                       -mag['FRN']['dBnMhd'] * np.cos((np.pi/2)-(30 * np.pi / 180)) * np.cos(LT * np.pi /12) - mag['FRN']['dBdMhd'] * np.sin((np.pi/2)-(30 * np.pi / 180)) * np.cos(LT * np.pi/12) - mag['FRN']['dBeMhd'] * np.sin(LT*np.pi/12),
                       -mag['IQA']['dBnMhd'] * np.cos((np.pi/2)-(35 * np.pi / 180)) * np.cos(LT * np.pi /12) - mag['IQA']['dBdMhd'] * np.sin((np.pi/2)-(35 * np.pi / 180)) * np.cos(LT * np.pi/12) - mag['IQA']['dBeMhd'] * np.sin(LT*np.pi/12),
                       -mag['PBQ']['dBnMhd'] * np.cos((np.pi/2)-(40 * np.pi / 180)) * np.cos(LT * np.pi /12) - mag['PBQ']['dBdMhd'] * np.sin((np.pi/2)-(40 * np.pi / 180)) * np.cos(LT * np.pi/12) - mag['PBQ']['dBeMhd'] * np.sin(LT*np.pi/12),
                       -mag['OTT']['dBnMhd'] * np.cos((np.pi/2)-(45 * np.pi / 180)) * np.cos(LT * np.pi /12) - mag['OTT']['dBdMhd'] * np.sin((np.pi/2)-(45 * np.pi / 180)) * np.cos(LT * np.pi/12) - mag['OTT']['dBeMhd'] * np.sin(LT*np.pi/12),
                       -mag['FRD']['dBnMhd'] * np.cos((np.pi/2)-(50 * np.pi / 180)) * np.cos(LT * np.pi /12) - mag['FRD']['dBdMhd'] * np.sin((np.pi/2)-(50 * np.pi / 180)) * np.cos(LT * np.pi/12) - mag['FRD']['dBeMhd'] * np.sin(LT*np.pi/12),
                       -mag['HRN']['dBnMhd'] * np.cos((np.pi/2)-(55 * np.pi / 180)) * np.cos(LT * np.pi /12) - mag['HRN']['dBdMhd'] * np.sin((np.pi/2)-(55 * np.pi / 180)) * np.cos(LT * np.pi/12) - mag['HRN']['dBeMhd'] * np.sin(LT*np.pi/12),
                       -mag['ABK']['dBnMhd'] * np.cos((np.pi/2)-(60 * np.pi / 180)) * np.cos(LT * np.pi /12) - mag['ABK']['dBdMhd'] * np.sin((np.pi/2)-(60 * np.pi / 180)) * np.cos(LT * np.pi/12) - mag['ABK']['dBeMhd'] * np.sin(LT*np.pi/12),
                       -mag['WNG']['dBnMhd'] * np.cos((np.pi/2)-(65 * np.pi / 180)) * np.cos(LT * np.pi /12) - mag['WNG']['dBdMhd'] * np.sin((np.pi/2)-(65 * np.pi / 180)) * np.cos(LT * np.pi/12) - mag['WNG']['dBeMhd'] * np.sin(LT*np.pi/12),
                       -mag['FUR']['dBnMhd'] * np.cos((np.pi/2)-(70 * np.pi / 180)) * np.cos(LT * np.pi /12) - mag['FUR']['dBdMhd'] * np.sin((np.pi/2)-(70 * np.pi / 180)) * np.cos(LT * np.pi/12) - mag['FUR']['dBeMhd'] * np.sin(LT*np.pi/12)])
                      
    mhd[1] = np.array([-mag['DST']['dBnMhd'] * np.cos((np.pi/2)-(10 * np.pi / 180)) * np.sin(LT * np.pi / 12) - mag['DST']['dBdMhd'] * np.sin((np.pi/2)-(10 * np.pi / 180)) * np.sin(LT * np.pi/12) + mag['DST']['dBeMhd'] * np.cos(LT*np.pi/12),
                       -mag['YKC']['dBnMhd'] * np.cos((np.pi/2)-(15 * np.pi / 180)) * np.sin(LT * np.pi / 12) - mag['YKC']['dBdMhd'] * np.sin((np.pi/2)-(15 * np.pi / 180)) * np.sin(LT * np.pi/12) + mag['YKC']['dBeMhd'] * np.cos(LT*np.pi/12),
                       -mag['MEA']['dBnMhd'] * np.cos((np.pi/2)-(20 * np.pi / 180)) * np.sin(LT * np.pi / 12) - mag['MEA']['dBdMhd'] * np.sin((np.pi/2)-(20 * np.pi / 180)) * np.sin(LT * np.pi/12) + mag['MEA']['dBeMhd'] * np.cos(LT*np.pi/12),
                       -mag['NEW']['dBnMhd'] * np.cos((np.pi/2)-(25 * np.pi / 180)) * np.sin(LT * np.pi / 12) - mag['NEW']['dBdMhd'] * np.sin((np.pi/2)-(25 * np.pi / 180)) * np.sin(LT * np.pi/12) + mag['NEW']['dBeMhd'] * np.cos(LT*np.pi/12),
                       -mag['FRN']['dBnMhd'] * np.cos((np.pi/2)-(30 * np.pi / 180)) * np.sin(LT * np.pi / 12) - mag['FRN']['dBdMhd'] * np.sin((np.pi/2)-(30 * np.pi / 180)) * np.sin(LT * np.pi/12) + mag['FRN']['dBeMhd'] * np.cos(LT*np.pi/12),
                       -mag['IQA']['dBnMhd'] * np.cos((np.pi/2)-(35 * np.pi / 180)) * np.sin(LT * np.pi / 12) - mag['IQA']['dBdMhd'] * np.sin((np.pi/2)-(35 * np.pi / 180)) * np.sin(LT * np.pi/12) + mag['IQA']['dBeMhd'] * np.cos(LT*np.pi/12),
                       -mag['PBQ']['dBnMhd'] * np.cos((np.pi/2)-(40 * np.pi / 180)) * np.sin(LT * np.pi / 12) - mag['PBQ']['dBdMhd'] * np.sin((np.pi/2)-(40 * np.pi / 180)) * np.sin(LT * np.pi/12) + mag['PBQ']['dBeMhd'] * np.cos(LT*np.pi/12),
                       -mag['OTT']['dBnMhd'] * np.cos((np.pi/2)-(45 * np.pi / 180)) * np.sin(LT * np.pi / 12) - mag['OTT']['dBdMhd'] * np.sin((np.pi/2)-(45 * np.pi / 180)) * np.sin(LT * np.pi/12) + mag['OTT']['dBeMhd'] * np.cos(LT*np.pi/12),
                       -mag['FRD']['dBnMhd'] * np.cos((np.pi/2)-(50 * np.pi / 180)) * np.sin(LT * np.pi / 12) - mag['FRD']['dBdMhd'] * np.sin((np.pi/2)-(50 * np.pi / 180)) * np.sin(LT * np.pi/12) + mag['FRD']['dBeMhd'] * np.cos(LT*np.pi/12),
                       -mag['HRN']['dBnMhd'] * np.cos((np.pi/2)-(55 * np.pi / 180)) * np.sin(LT * np.pi / 12) - mag['HRN']['dBdMhd'] * np.sin((np.pi/2)-(55 * np.pi / 180)) * np.sin(LT * np.pi/12) + mag['HRN']['dBeMhd'] * np.cos(LT*np.pi/12),
                       -mag['ABK']['dBnMhd'] * np.cos((np.pi/2)-(60 * np.pi / 180)) * np.sin(LT * np.pi / 12) - mag['ABK']['dBdMhd'] * np.sin((np.pi/2)-(60 * np.pi / 180)) * np.sin(LT * np.pi/12) + mag['ABK']['dBeMhd'] * np.cos(LT*np.pi/12),
                       -mag['WNG']['dBnMhd'] * np.cos((np.pi/2)-(65 * np.pi / 180)) * np.sin(LT * np.pi / 12) - mag['WNG']['dBdMhd'] * np.sin((np.pi/2)-(65 * np.pi / 180)) * np.sin(LT * np.pi/12) + mag['WNG']['dBeMhd'] * np.cos(LT*np.pi/12),
                       -mag['FUR']['dBnMhd'] * np.cos((np.pi/2)-(70 * np.pi / 180)) * np.sin(LT * np.pi / 12) - mag['FUR']['dBdMhd'] * np.sin((np.pi/2)-(70 * np.pi / 180)) * np.sin(LT * np.pi/12) + mag['FUR']['dBeMhd'] * np.cos(LT*np.pi/12)])
                       
    mhd[2] = np.array([mag['DST']['dBnMhd'] * np.sin((np.pi/2)-(10 * np.pi / 180)) - mag['DST']['dBdMhd'] * np.cos((np.pi/2)-(10 * np.pi / 180)),
                       mag['YKC']['dBnMhd'] * np.sin((np.pi/2)-(15 * np.pi / 180)) - mag['YKC']['dBdMhd'] * np.cos((np.pi/2)-(15 * np.pi / 180)),
                       mag['MEA']['dBnMhd'] * np.sin((np.pi/2)-(20 * np.pi / 180)) - mag['MEA']['dBdMhd'] * np.cos((np.pi/2)-(20 * np.pi / 180)),
                       mag['NEW']['dBnMhd'] * np.sin((np.pi/2)-(25 * np.pi / 180)) - mag['NEW']['dBdMhd'] * np.cos((np.pi/2)-(25 * np.pi / 180)),
                       mag['FRN']['dBnMhd'] * np.sin((np.pi/2)-(30 * np.pi / 180)) - mag['FRN']['dBdMhd'] * np.cos((np.pi/2)-(30 * np.pi / 180)),
                       mag['IQA']['dBnMhd'] * np.sin((np.pi/2)-(35 * np.pi / 180)) - mag['IQA']['dBdMhd'] * np.cos((np.pi/2)-(35 * np.pi / 180)),
                       mag['PBQ']['dBnMhd'] * np.sin((np.pi/2)-(40 * np.pi / 180)) - mag['PBQ']['dBdMhd'] * np.cos((np.pi/2)-(40 * np.pi / 180)),
                       mag['OTT']['dBnMhd'] * np.sin((np.pi/2)-(45 * np.pi / 180)) - mag['OTT']['dBdMhd'] * np.cos((np.pi/2)-(45 * np.pi / 180)),
                       mag['FRD']['dBnMhd'] * np.sin((np.pi/2)-(50 * np.pi / 180)) - mag['FRD']['dBdMhd'] * np.cos((np.pi/2)-(50 * np.pi / 180)),
                       mag['HRN']['dBnMhd'] * np.sin((np.pi/2)-(55 * np.pi / 180)) - mag['HRN']['dBdMhd'] * np.cos((np.pi/2)-(55 * np.pi / 180)),
                       mag['ABK']['dBnMhd'] * np.sin((np.pi/2)-(60 * np.pi / 180)) - mag['ABK']['dBdMhd'] * np.cos((np.pi/2)-(60 * np.pi / 180)),
                       mag['WNG']['dBnMhd'] * np.sin((np.pi/2)-(65 * np.pi / 180)) - mag['WNG']['dBdMhd'] * np.cos((np.pi/2)-(65 * np.pi / 180)),
                       mag['FUR']['dBnMhd'] * np.sin((np.pi/2)-(70 * np.pi / 180)) - mag['FUR']['dBdMhd'] * np.cos((np.pi/2)-(70 * np.pi / 180))])
                       
    return t, mhd

LT00 = mhd('SWMF/run_test/GM/IO2/magnetometers_e20150321-054500.mag')

style()

custom_lines = [Line2D([0], [0], color='#ff6961', lw=1)]

for number in range(881):
    fig, ax = plt.subplots()
    for num, item in enumerate(LT00[1][1]):
        ax.plot(LT00[0], LT00[1][2][num], color = '#ff6961')


    frame = datetime(2015, 3, 21, 6, 00, 20) + timedelta(seconds = number)
    box = plt.gca().get_position()
    #ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    #ax.legend(custom_lines, ['LT00', 'LT03', 'LT06', 'LT09', 'LT12', 'LT15', 'LT18', 'LT21'], loc='center left', bbox_to_anchor=(1, 0.5), frameon = True)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.axvline(x = frame, linestyle = 'dotted', color = 'black')
    plt.ylim(-300, 200)
    plt.xlim((datetime(2015, 3, 21, 6, 00, 20), datetime(2015, 3, 21, 6, 15, 0)))
    #plt.xticks(np.arange(datetime(2015, 3, 21, 5, 58, 00), datetime(2015, 3, 21, 6, 3, 0), timedelta(minutes = 1)).astype(datetime))
    plt.title(r'$B_z \ vs. \ UT$'+'\n'+f"{frame.hour:02}"+':'+f"{frame.minute:02}"+':'+f"{frame.second:02}")
    plt.ylabel(r'$B_z \ (nT)$')
    plt.xlabel('UT (HH:MM)')
    plt.tick_params(rotation=45)
    plt.savefig('test2/'+f"{frame.hour:02}"+f"{frame.minute:02}"+f"{frame.second:02}"+'.png', bbox_inches='tight')
    plt.close()
'''
fig, ax = plt.subplots()
for num, item in enumerate(LT00[1][1]):
        ax.plot(LT00[0], LT00[1][0][num], color = '#ff6961')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.title(r'$B_x \ vs. \ UT$')
plt.ylabel(r'$B_x \ (nT)$')
plt.xlabel('UT (HH:MM)')
plt.tick_params(rotation=45)
plt.savefig('precursorDB/docs/EventList/SEA/ideal_ssc/newrun/simSEA/x.png', bbox_inches='tight')
plt.show()

fig, ax = plt.subplots()
for num, item in enumerate(LT00[1][1]):
        ax.plot(LT00[0], LT00[1][1][num], color = '#ff6961')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.title(r'$B_y \ vs. \ UT$')
plt.ylabel(r'$B_y \ (nT)$')
plt.xlabel('UT (HH:MM)')
plt.tick_params(rotation=45)
plt.savefig('precursorDB/docs/EventList/SEA/ideal_ssc/newrun/simSEA/y.png', bbox_inches='tight')
plt.show()

fig, ax = plt.subplots()
for num, item in enumerate(LT00[1][1]):
        ax.plot(LT00[0], LT00[1][2][num], color = '#ff6961')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.title(r'$B_z \ vs. \ UT$')
plt.ylabel(r'$B_z \ (nT)$')
plt.xlabel('UT (HH:MM)')
plt.tick_params(rotation=45)
plt.savefig('precursorDB/docs/EventList/SEA/ideal_ssc/newrun/simSEA/z.png', bbox_inches='tight')
plt.show()
'''