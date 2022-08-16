import matplotlib.pyplot as plt; plt.ion()
from spacepy.pybats import bats
from datetime import datetime
import matplotlib.dates as mdates
import numpy as np
from spacepy.plot import style
from matplotlib.lines import Line2D

#function to break precursor into components
def abs(filename):
	LT = int(filename[-11:-9])
	maglat = 10
	mag = bats.MagFile(filename)
	t = mag['time']
	plotlen = len(mag['time'])
	mhd, hal, ped, fac, full = [], [], [], [], []

    #convert MHD, Hall, Pederson, and FAC vectors to SM coordinates
	maglat = 10
	while maglat <= 80:
		for num, item in enumerate(mag['time']):
			mhd.append(np.sqrt(mag['d'+str(maglat)]['dBnMhd'][num]**2 + mag['d'+str(maglat)]['dBdMhd'][num]**2 + mag['d'+str(maglat)]['dBeMhd'][num]**2))
			hal.append(np.sqrt(mag['d'+str(maglat)]['dBnHal'][num]**2 + mag['d'+str(maglat)]['dBdHal'][num]**2 + mag['d'+str(maglat)]['dBeHal'][num]**2))
			ped.append(np.sqrt(mag['d'+str(maglat)]['dBnPed'][num]**2 + mag['d'+str(maglat)]['dBdPed'][num]**2 + mag['d'+str(maglat)]['dBePed'][num]**2))
			fac.append(np.sqrt(mag['d'+str(maglat)]['dBnFac'][num]**2 + mag['d'+str(maglat)]['dBdFac'][num]**2 + mag['d'+str(maglat)]['dBeFac'][num]**2))
			full.append(np.sqrt(mag['d'+str(maglat)]['dBn'][num]**2 + mag['d'+str(maglat)]['dBd'][num]**2 + mag['d'+str(maglat)]['dBe'][num]**2))
		maglat += 5
	
	full=np.array_split(full, len(full)/plotlen)
	mhd=np.array_split(mhd, len(mhd)/plotlen)
	hal=np.array_split(hal, len(hal)/plotlen)
	ped=np.array_split(ped, len(ped)/plotlen)
	fac=np.array_split(fac, len(fac)/plotlen)
    
	return t, mhd, hal, ped, fac, full

#take the absolute value of each component
LT00 = abs('MHD/LT_00_mags.mag')
LT03 = abs('MHD/LT_03_mags.mag')
LT06 = abs('MHD/LT_06_mags.mag')
LT09 = abs('MHD/LT_09_mags.mag')
LT12 = abs('MHD/LT_12_mags.mag')
LT15 = abs('MHD/LT_15_mags.mag')
LT18 = abs('MHD/LT_18_mags.mag')
LT21 = abs('MHD/LT_21_mags.mag')

custom_lines = [Line2D([0], [0], color='red', lw=1),
                Line2D([0], [0], color='orange', lw=1),
                Line2D([0], [0], color='yellow', lw=1),
                Line2D([0], [0], color='green', lw=1),
                Line2D([0], [0], color='blue', lw=1),
                Line2D([0], [0], color='indigo', lw=1),
                Line2D([0], [0], color='violet', lw=1),
                Line2D([0], [0], color='gray', lw=1)]

style()

#plot MHD contribution
fig, ax = plt.subplots()
for num, item in enumerate(LT00[1]):
	plot1, = plt.plot(LT00[0], LT00[1][num], color = 'red')
	plot2, = plt.plot(LT00[0], LT03[1][num], color = 'orange')
	plot3, = plt.plot(LT00[0], LT06[1][num], color = 'yellow')
	plot4, = plt.plot(LT00[0], LT09[1][num], color = 'green')
	plot5, = plt.plot(LT00[0], LT12[1][num], color = 'blue')
	plot6, = plt.plot(LT00[0], LT15[1][num], color = 'indigo')
	plot7, = plt.plot(LT00[0], LT18[1][num], color = 'violet')
	plot8, = plt.plot(LT00[0], LT21[1][num], color = 'gray')
box = plt.gca().get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(custom_lines, ['LT00', 'LT03', 'LT06', 'LT09', 'LT12', 'LT15', 'LT18', 'LT21'], loc='center left', bbox_to_anchor=(1, 0.5), frameon = True)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.axvline(x = datetime(2015, 3, 21, 6, 00), linestyle = 'dotted', color = 'black')
plt.xlim((LT00[0][0],LT00[0][2000]))
plt.title('Absolute Value of MHD Contribution')
plt.ylabel(r'$B \ (nT)$')
plt.xlabel('UT (HH:MM)')
plt.savefig('precursorDB/docs/EventList/SEA/ideal_ssc/absolute_value/MHD.png')

#plot Hall current contribution
fig, ax = plt.subplots()
for num, item in enumerate(LT00[2]):
	plot1, = plt.plot(LT00[0], LT00[2][num], color = 'red')
	plot2, = plt.plot(LT00[0], LT03[2][num], color = 'orange')
	plot3, = plt.plot(LT00[0], LT06[2][num], color = 'yellow')
	plot4, = plt.plot(LT00[0], LT09[2][num], color = 'green')
	plot5, = plt.plot(LT00[0], LT12[2][num], color = 'blue')
	plot6, = plt.plot(LT00[0], LT15[2][num], color = 'indigo')
	plot7, = plt.plot(LT00[0], LT18[2][num], color = 'violet')
	plot8, = plt.plot(LT00[0], LT21[2][num], color = 'gray')
box = plt.gca().get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(custom_lines, ['LT00', 'LT03', 'LT06', 'LT09', 'LT12', 'LT15', 'LT18', 'LT21'], loc='center left', bbox_to_anchor=(1, 0.5), frameon = True)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.axvline(x = datetime(2015, 3, 21, 6, 00), linestyle = 'dotted', color = 'black')
plt.xlim((LT00[0][0],LT00[0][2000]))
plt.title('Absolute Value of Hall Current Contribution')
plt.ylabel(r'$B \ (nT)$')
plt.xlabel('UT (HH:MM)')
plt.savefig('precursorDB/docs/EventList/SEA/ideal_ssc/absolute_value/Hall.png')

#plot Pederson current contribution
fig, ax = plt.subplots()
for num, item in enumerate(LT00[3]):
	plot1, = plt.plot(LT00[0], LT00[3][num], color = 'red')
	plot2, = plt.plot(LT00[0], LT03[3][num], color = 'orange')
	plot3, = plt.plot(LT00[0], LT06[3][num], color = 'yellow')
	plot4, = plt.plot(LT00[0], LT09[3][num], color = 'green')
	plot5, = plt.plot(LT00[0], LT12[3][num], color = 'blue')
	plot6, = plt.plot(LT00[0], LT15[3][num], color = 'indigo')
	plot7, = plt.plot(LT00[0], LT18[3][num], color = 'violet')
	plot8, = plt.plot(LT00[0], LT21[3][num], color = 'gray')
box = plt.gca().get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(custom_lines, ['LT00', 'LT03', 'LT06', 'LT09', 'LT12', 'LT15', 'LT18', 'LT21'], loc='center left', bbox_to_anchor=(1, 0.5), frameon = True)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.axvline(x = datetime(2015, 3, 21, 6, 00), linestyle = 'dotted', color = 'black')
plt.xlim((LT00[0][0],LT00[0][2000]))
plt.title('Absolute Value of Pederson Current Contribution')
plt.ylabel(r'$B \ (nT)$')
plt.xlabel('UT (HH:MM)')
plt.savefig('precursorDB/docs/EventList/SEA/ideal_ssc/absolute_value/Pederson.png')

#plot FAC contribution
fig, ax = plt.subplots()
for num, item in enumerate(LT00[4]):
	plot1, = plt.plot(LT00[0], LT00[4][num], color = 'red')
	plot2, = plt.plot(LT00[0], LT03[4][num], color = 'orange')
	plot3, = plt.plot(LT00[0], LT06[4][num], color = 'yellow')
	plot4, = plt.plot(LT00[0], LT09[4][num], color = 'green')
	plot5, = plt.plot(LT00[0], LT12[4][num], color = 'blue')
	plot6, = plt.plot(LT00[0], LT15[4][num], color = 'indigo')
	plot7, = plt.plot(LT00[0], LT18[4][num], color = 'violet')
	plot8, = plt.plot(LT00[0], LT21[4][num], color = 'gray')
box = plt.gca().get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(custom_lines, ['LT00', 'LT03', 'LT06', 'LT09', 'LT12', 'LT15', 'LT18', 'LT21'], loc='center left', bbox_to_anchor=(1, 0.5), frameon = True)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.axvline(x = datetime(2015, 3, 21, 6, 00), linestyle = 'dotted', color = 'black')
plt.xlim((LT00[0][0],LT00[0][2000]))
plt.title('Absolute Value of FAC Contribution')
plt.ylabel(r'$B \ (nT)$')
plt.xlabel('UT (HH:MM)')
plt.savefig('precursorDB/docs/EventList/SEA/ideal_ssc/absolute_value/FAC.png')

#plot all contributions
fig, ax = plt.subplots()
for num, item in enumerate(LT00[4]):
	plot1, = plt.plot(LT00[0], LT00[5][num], color = 'red')
	plot2, = plt.plot(LT00[0], LT03[5][num], color = 'orange')
	plot3, = plt.plot(LT00[0], LT06[5][num], color = 'yellow')
	plot4, = plt.plot(LT00[0], LT09[5][num], color = 'green')
	plot5, = plt.plot(LT00[0], LT12[5][num], color = 'blue')
	plot6, = plt.plot(LT00[0], LT15[5][num], color = 'indigo')
	plot7, = plt.plot(LT00[0], LT18[5][num], color = 'violet')
	plot8, = plt.plot(LT00[0], LT21[5][num], color = 'gray')
box = plt.gca().get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(custom_lines, ['LT00', 'LT03', 'LT06', 'LT09', 'LT12', 'LT15', 'LT18', 'LT21'], loc='center left', bbox_to_anchor=(1, 0.5), frameon = True)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.axvline(x = datetime(2015, 3, 21, 6, 00), linestyle = 'dotted', color = 'black')
plt.xlim((LT00[0][0],LT00[0][2000]))
plt.title('Absolute Value of All Contributions')
plt.ylabel(r'$B \ (nT)$')
plt.xlabel('UT (HH:MM)')
plt.savefig('precursorDB/docs/EventList/SEA/ideal_ssc/absolute_value/AllContributions.png')