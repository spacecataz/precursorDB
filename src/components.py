import matplotlib.pyplot as plt; plt.ion()
from spacepy.pybats import bats
from datetime import datetime
import matplotlib.dates as mdates
import numpy as np
from spacepy.plot import style
from matplotlib.lines import Line2D

#function to break precursor into components
def components(filename):
	LT = int(filename[-11:-9])
	maglat = 10
	mag = bats.MagFile(filename)
	t = mag['time']
	plotlen = len(mag['time'])
	mhdsmx, mhdsmy, mhdsmz = [], [], []
	hallsmx, hallsmy, hallsmz = [], [], []
	pedsmx, pedsmy, pedsmz = [], [], []
	facsmx, facsmy, facsmz = [], [], []

	#convert MHD, Hall, Pederson, and FAC vectors to SM coordinates
	maglat = 10
	while maglat <= 80:
		for num, item in enumerate(mag['time']):
			mhdsmx.append(-mag['d'+str(maglat)]['dBnMhd'][num] * np.cos((np.pi/2)-(maglat * np.pi / 180)) * np.cos(LT * np.pi /12) - mag['d'+str(maglat)]['dBdMhd'][num] * np.sin((np.pi/2)-(maglat * np.pi / 180)) * np.cos(LT * np.pi/12) - mag['d'+str(maglat)]['dBeMhd'][num] * np.sin(LT*np.pi/12))
			mhdsmy.append(-mag['d'+str(maglat)]['dBnMhd'][num] * np.cos((np.pi/2)-(maglat * np.pi / 180)) * np.sin(LT * np.pi / 12) - mag['d'+str(maglat)]['dBdMhd'][num] * np.sin((np.pi/2)-(maglat * np.pi / 180)) * np.sin(LT * np.pi/12) + mag['d'+str(maglat)]['dBeMhd'][num] * np.cos(LT*np.pi/12))
			mhdsmz.append(mag['d'+str(maglat)]['dBnMhd'][num] * np.sin((np.pi/2)-(maglat * np.pi / 180)) - mag['d'+str(maglat)]['dBdMhd'][num] * np.cos((np.pi/2)-(maglat * np.pi / 180)))
			hallsmx.append(-mag['d'+str(maglat)]['dBnHal'][num] * np.cos((np.pi/2)-(maglat * np.pi / 180)) * np.cos(LT * np.pi /12) - mag['d'+str(maglat)]['dBdHal'][num] * np.sin((np.pi/2)-(maglat * np.pi / 180)) * np.cos(LT * np.pi/12) - mag['d'+str(maglat)]['dBeHal'][num] * np.sin(LT*np.pi/12))
			hallsmy.append(-mag['d'+str(maglat)]['dBnHal'][num] * np.cos((np.pi/2)-(maglat * np.pi / 180)) * np.sin(LT * np.pi / 12) - mag['d'+str(maglat)]['dBdHal'][num] * np.sin((np.pi/2)-(maglat * np.pi / 180)) * np.sin(LT * np.pi/12) + mag['d'+str(maglat)]['dBeHal'][num] * np.cos(LT*np.pi/12))
			hallsmz.append(mag['d'+str(maglat)]['dBnHal'][num] * np.sin((np.pi/2)-(maglat * np.pi / 180)) - mag['d'+str(maglat)]['dBdHal'][num] * np.cos((np.pi/2)-(maglat * np.pi / 180)))
			pedsmx.append(-mag['d'+str(maglat)]['dBnPed'][num] * np.cos((np.pi/2)-(maglat * np.pi / 180)) * np.cos(LT * np.pi /12) - mag['d'+str(maglat)]['dBdPed'][num] * np.sin((np.pi/2)-(maglat * np.pi / 180)) * np.cos(LT * np.pi/12) - mag['d'+str(maglat)]['dBePed'][num] * np.sin(LT*np.pi/12))
			pedsmy.append(-mag['d'+str(maglat)]['dBnPed'][num] * np.cos((np.pi/2)-(maglat * np.pi / 180)) * np.sin(LT * np.pi / 12) - mag['d'+str(maglat)]['dBdPed'][num] * np.sin((np.pi/2)-(maglat * np.pi / 180)) * np.sin(LT * np.pi/12) + mag['d'+str(maglat)]['dBePed'][num] * np.cos(LT*np.pi/12))
			pedsmz.append(mag['d'+str(maglat)]['dBnPed'][num] * np.sin((np.pi/2)-(maglat * np.pi / 180)) - mag['d'+str(maglat)]['dBdPed'][num] * np.cos((np.pi/2)-(maglat * np.pi / 180)))
			facsmx.append(-mag['d'+str(maglat)]['dBnFac'][num] * np.cos((np.pi/2)-(maglat * np.pi / 180)) * np.cos(LT * np.pi /12) - mag['d'+str(maglat)]['dBdFac'][num] * np.sin((np.pi/2)-(maglat * np.pi / 180)) * np.cos(LT * np.pi/12) - mag['d'+str(maglat)]['dBeFac'][num] * np.sin(LT*np.pi/12))
			facsmy.append(-mag['d'+str(maglat)]['dBnFac'][num] * np.cos((np.pi/2)-(maglat * np.pi / 180)) * np.sin(LT * np.pi / 12) - mag['d'+str(maglat)]['dBdFac'][num] * np.sin((np.pi/2)-(maglat * np.pi / 180)) * np.sin(LT * np.pi/12) + mag['d'+str(maglat)]['dBeFac'][num] * np.cos(LT*np.pi/12))
			facsmz.append(mag['d'+str(maglat)]['dBnFac'][num] * np.sin((np.pi/2)-(maglat * np.pi / 180)) - mag['d'+str(maglat)]['dBdFac'][num] * np.cos((np.pi/2)-(maglat * np.pi / 180)))
		maglat += 5
	
	mhdsmx=np.array_split(mhdsmx, len(mhdsmx)/plotlen)
	mhdsmy=np.array_split(mhdsmy, len(mhdsmy)/plotlen)
	mhdsmz=np.array_split(mhdsmz, len(mhdsmz)/plotlen)
	hallsmx=np.array_split(hallsmx, len(hallsmx)/plotlen)
	hallsmy=np.array_split(hallsmy, len(hallsmy)/plotlen)
	hallsmz=np.array_split(hallsmz, len(hallsmz)/plotlen)
	pedsmx=np.array_split(pedsmx, len(pedsmx)/plotlen)
	pedsmy=np.array_split(pedsmy, len(pedsmy)/plotlen)
	pedsmz=np.array_split(pedsmz, len(pedsmz)/plotlen)
	facsmx=np.array_split(facsmx, len(facsmx)/plotlen)
	facsmy=np.array_split(facsmy, len(facsmy)/plotlen)
	facsmz=np.array_split(facsmz, len(facsmz)/plotlen)

    
	return t, mhdsmx, mhdsmy, mhdsmz, hallsmx, hallsmy, hallsmz, pedsmx, pedsmy, pedsmz, facsmx, facsmy, facsmz

LT00 = components('MHD/LT_00_mags.mag')
LT03 = components('MHD/LT_03_mags.mag')
LT06 = components('MHD/LT_06_mags.mag')
LT09 = components('MHD/LT_09_mags.mag')
LT12 = components('MHD/LT_12_mags.mag')
LT15 = components('MHD/LT_15_mags.mag')
LT18 = components('MHD/LT_18_mags.mag')
LT21 = components('MHD/LT_21_mags.mag')

custom_lines = [Line2D([0], [0], color='red', lw=1),
                Line2D([0], [0], color='orange', lw=1),
                Line2D([0], [0], color='yellow', lw=1),
                Line2D([0], [0], color='green', lw=1),
                Line2D([0], [0], color='blue', lw=1),
                Line2D([0], [0], color='indigo', lw=1),
                Line2D([0], [0], color='violet', lw=1),
                Line2D([0], [0], color='gray', lw=1)]

style()

#plot MHD contribution in X direction
fig, ax = plt.subplots()
for num in range(len(LT00[1])):
	ax.plot(LT00[0], LT00[1][num], color = 'red')
	ax.plot(LT00[0], LT03[1][num], color = 'orange')
	ax.plot(LT00[0], LT06[1][num], color = 'yellow')
	ax.plot(LT00[0], LT09[1][num], color = 'green')
	ax.plot(LT00[0], LT12[1][num], color = 'blue')
	ax.plot(LT00[0], LT15[1][num], color = 'indigo')
	ax.plot(LT00[0], LT18[1][num], color = 'violet')
	ax.plot(LT00[0], LT21[1][num], color = 'gray')
box = plt.gca().get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(custom_lines, ['LT00', 'LT03', 'LT06', 'LT09', 'LT12', 'LT15', 'LT18', 'LT21'], loc='center left', bbox_to_anchor=(1, 0.5), frameon = True)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.axvline(x = datetime(2015, 3, 21, 6, 00), linestyle = 'dotted', color = 'black')
plt.xlim((LT00[0][0],LT00[0][2000]))
plt.title('MHD Contribution in the X-Direction')
plt.ylabel(r'$B \ (nT)$')
plt.xlabel('UT (HH:MM)')
plt.savefig('precursorDB/docs/EventList/SEA/ideal_ssc/SM/MHD/MHD_x.png')

#plot MHD contribution in Y direction
fig, ax = plt.subplots()
for num, item in enumerate(LT00[1]):
	ax.plot(LT00[0], LT00[2][num], color = 'red')
	ax.plot(LT00[0], LT03[2][num], color = 'orange')
	ax.plot(LT00[0], LT06[2][num], color = 'yellow')
	ax.plot(LT00[0], LT09[2][num], color = 'green')
	ax.plot(LT00[0], LT12[2][num], color = 'blue')
	ax.plot(LT00[0], LT15[2][num], color = 'indigo')
	ax.plot(LT00[0], LT18[2][num], color = 'violet')
	ax.plot(LT00[0], LT21[2][num], color = 'gray')
box = plt.gca().get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(custom_lines, ['LT00', 'LT03', 'LT06', 'LT09', 'LT12', 'LT15', 'LT18', 'LT21'], loc='center left', bbox_to_anchor=(1, 0.5), frameon = True)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.axvline(x = datetime(2015, 3, 21, 6, 00), linestyle = 'dotted', color = 'black')
plt.xlim((LT00[0][0],LT00[0][2000]))
plt.title('MHD Contribution in the Y-Direction')
plt.ylabel(r'$B \ (nT)$')
plt.xlabel('UT (HH:MM)')
plt.savefig('precursorDB/docs/EventList/SEA/ideal_ssc/SM/MHD/MHD_y.png')

#plot MHD contribution in Z direction
fig, ax = plt.subplots()
for num, item in enumerate(LT00[1]):
	ax.plot(LT00[0], LT00[3][num], color = 'red')
	ax.plot(LT00[0], LT03[3][num], color = 'orange')
	ax.plot(LT00[0], LT06[3][num], color = 'yellow')
	ax.plot(LT00[0], LT09[3][num], color = 'green')
	ax.plot(LT00[0], LT12[3][num], color = 'blue')
	ax.plot(LT00[0], LT15[3][num], color = 'indigo')
	ax.plot(LT00[0], LT18[3][num], color = 'violet')
	ax.plot(LT00[0], LT21[3][num], color = 'gray')
box = plt.gca().get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(custom_lines, ['LT00', 'LT03', 'LT06', 'LT09', 'LT12', 'LT15', 'LT18', 'LT21'], loc='center left', bbox_to_anchor=(1, 0.5), frameon = True)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.axvline(x = datetime(2015, 3, 21, 6, 00), linestyle = 'dotted', color = 'black')
plt.xlim((LT00[0][0],LT00[0][2000]))
plt.title('MHD Contribution in the Z-Direction')
plt.ylabel(r'$B \ (nT)$')
plt.xlabel('UT (HH:MM)')
plt.savefig('precursorDB/docs/EventList/SEA/ideal_ssc/SM/MHD/MHD_z.png')

#plot Hall current contribution in X direction
fig, ax = plt.subplots()
for num, item in enumerate(LT00[1]):
	ax.plot(LT00[0], LT00[4][num], color = 'red')
	ax.plot(LT00[0], LT03[4][num], color = 'orange')
	ax.plot(LT00[0], LT06[4][num], color = 'yellow')
	ax.plot(LT00[0], LT09[4][num], color = 'green')
	ax.plot(LT00[0], LT12[4][num], color = 'blue')
	ax.plot(LT00[0], LT15[4][num], color = 'indigo')
	ax.plot(LT00[0], LT18[4][num], color = 'violet')
	ax.plot(LT00[0], LT21[4][num], color = 'gray')
box = plt.gca().get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(custom_lines, ['LT00', 'LT03', 'LT06', 'LT09', 'LT12', 'LT15', 'LT18', 'LT21'], loc='center left', bbox_to_anchor=(1, 0.5), frameon = True)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.axvline(x = datetime(2015, 3, 21, 6, 00), linestyle = 'dotted', color = 'black')
plt.xlim((LT00[0][0],LT00[0][2000]))
plt.title('Hall Current Contribution in the X-Direction')
plt.ylabel(r'$B \ (nT)$')
plt.xlabel('UT (HH:MM)')
plt.savefig('precursorDB/docs/EventList/SEA/ideal_ssc/SM/Hall/Hall_x.png')

#plot Hall current contribution in Y direction
fig, ax = plt.subplots()
for num, item in enumerate(LT00[1]):
	ax.plot(LT00[0], LT00[5][num], color = 'red')
	ax.plot(LT00[0], LT03[5][num], color = 'orange')
	ax.plot(LT00[0], LT06[5][num], color = 'yellow')
	ax.plot(LT00[0], LT09[5][num], color = 'green')
	ax.plot(LT00[0], LT12[5][num], color = 'blue')
	ax.plot(LT00[0], LT15[5][num], color = 'indigo')
	ax.plot(LT00[0], LT18[5][num], color = 'violet')
	ax.plot(LT00[0], LT21[5][num], color = 'gray')
box = plt.gca().get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(custom_lines, ['LT00', 'LT03', 'LT06', 'LT09', 'LT12', 'LT15', 'LT18', 'LT21'], loc='center left', bbox_to_anchor=(1, 0.5), frameon = True)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.axvline(x = datetime(2015, 3, 21, 6, 00), linestyle = 'dotted', color = 'black')
plt.xlim((LT00[0][0],LT00[0][2000]))
plt.title('Hall Current Contribution in the Y-Direction')
plt.ylabel(r'$B \ (nT)$')
plt.xlabel('UT (HH:MM)')
plt.savefig('precursorDB/docs/EventList/SEA/ideal_ssc/SM/Hall/Hall_y.png')

#plot Hall current contribution in Z direction
fig, ax = plt.subplots()
for num, item in enumerate(LT00[1]):
	ax.plot(LT00[0], LT00[6][num], color = 'red')
	ax.plot(LT00[0], LT03[6][num], color = 'orange')
	ax.plot(LT00[0], LT06[6][num], color = 'yellow')
	ax.plot(LT00[0], LT09[6][num], color = 'green')
	ax.plot(LT00[0], LT12[6][num], color = 'blue')
	ax.plot(LT00[0], LT15[6][num], color = 'indigo')
	ax.plot(LT00[0], LT18[6][num], color = 'violet')
	ax.plot(LT00[0], LT21[6][num], color = 'gray')
box = plt.gca().get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(custom_lines, ['LT00', 'LT03', 'LT06', 'LT09', 'LT12', 'LT15', 'LT18', 'LT21'], loc='center left', bbox_to_anchor=(1, 0.5), frameon = True)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.axvline(x = datetime(2015, 3, 21, 6, 00), linestyle = 'dotted', color = 'black')
plt.xlim((LT00[0][0],LT00[0][2000]))
plt.title('Hall Current Contribution in the Z-Direction')
plt.ylabel(r'$B \ (nT)$')
plt.xlabel('UT (HH:MM)')
plt.savefig('precursorDB/docs/EventList/SEA/ideal_ssc/SM/Hall/Hall_z.png')

#plot Pederson current contribution in X direction
fig, ax = plt.subplots()
for num, item in enumerate(LT00[1]):
	ax.plot(LT00[0], LT00[7][num], color = 'red')
	ax.plot(LT00[0], LT03[7][num], color = 'orange')
	ax.plot(LT00[0], LT06[7][num], color = 'yellow')
	ax.plot(LT00[0], LT09[7][num], color = 'green')
	ax.plot(LT00[0], LT12[7][num], color = 'blue')
	ax.plot(LT00[0], LT15[7][num], color = 'indigo')
	ax.plot(LT00[0], LT18[7][num], color = 'violet')
	ax.plot(LT00[0], LT21[7][num], color = 'gray')
box = plt.gca().get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(custom_lines, ['LT00', 'LT03', 'LT06', 'LT09', 'LT12', 'LT15', 'LT18', 'LT21'], loc='center left', bbox_to_anchor=(1, 0.5), frameon = True)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.axvline(x = datetime(2015, 3, 21, 6, 00), linestyle = 'dotted', color = 'black')
plt.xlim((LT00[0][0],LT00[0][2000]))
plt.title('Pederson Current Contribution in the X-Direction')
plt.ylabel(r'$B \ (nT)$')
plt.xlabel('UT (HH:MM)')
plt.savefig('precursorDB/docs/EventList/SEA/ideal_ssc/SM/Pederson/Pederson_x.png')

#plot Pederson current contribution in Y direction
fig, ax = plt.subplots()
for num, item in enumerate(LT00[1]):
	ax.plot(LT00[0], LT00[8][num], color = 'red')
	ax.plot(LT00[0], LT03[8][num], color = 'orange')
	ax.plot(LT00[0], LT06[8][num], color = 'yellow')
	ax.plot(LT00[0], LT09[8][num], color = 'green')
	ax.plot(LT00[0], LT12[8][num], color = 'blue')
	ax.plot(LT00[0], LT15[8][num], color = 'indigo')
	ax.plot(LT00[0], LT18[8][num], color = 'violet')
	ax.plot(LT00[0], LT21[8][num], color = 'gray')
box = plt.gca().get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(custom_lines, ['LT00', 'LT03', 'LT06', 'LT09', 'LT12', 'LT15', 'LT18', 'LT21'], loc='center left', bbox_to_anchor=(1, 0.5), frameon = True)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.axvline(x = datetime(2015, 3, 21, 6, 00), linestyle = 'dotted', color = 'black')
plt.xlim((LT00[0][0],LT00[0][2000]))
plt.title('Pederson Current Contribution in the Y-Direction')
plt.ylabel(r'$B \ (nT)$')
plt.xlabel('UT (HH:MM)')
plt.savefig('precursorDB/docs/EventList/SEA/ideal_ssc/SM/Pederson/Pederson_y.png')

#plot Pederson current contribution in Z direction
fig, ax = plt.subplots()
for num, item in enumerate(LT00[1]):
	ax.plot(LT00[0], LT00[9][num], color = 'red')
	ax.plot(LT00[0], LT03[9][num], color = 'orange')
	ax.plot(LT00[0], LT06[9][num], color = 'yellow')
	ax.plot(LT00[0], LT09[9][num], color = 'green')
	ax.plot(LT00[0], LT12[9][num], color = 'blue')
	ax.plot(LT00[0], LT15[9][num], color = 'indigo')
	ax.plot(LT00[0], LT18[9][num], color = 'violet')
	ax.plot(LT00[0], LT21[9][num], color = 'gray')
box = plt.gca().get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(custom_lines, ['LT00', 'LT03', 'LT06', 'LT09', 'LT12', 'LT15', 'LT18', 'LT21'], loc='center left', bbox_to_anchor=(1, 0.5), frameon = True)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.axvline(x = datetime(2015, 3, 21, 6, 00), linestyle = 'dotted', color = 'black')
plt.xlim((LT00[0][0],LT00[0][2000]))
plt.title('Pederson Current Contribution in the Z-Direction')
plt.ylabel(r'$B \ (nT)$')
plt.xlabel('UT (HH:MM)')
plt.savefig('precursorDB/docs/EventList/SEA/ideal_ssc/SM/Pederson/Pederson_z.png')

#plot FAC contribution in X direction
fig, ax = plt.subplots()
for num, item in enumerate(LT00[1]):
	ax.plot(LT00[0], LT00[10][num], color = 'red')
	ax.plot(LT00[0], LT03[10][num], color = 'orange')
	ax.plot(LT00[0], LT06[10][num], color = 'yellow')
	ax.plot(LT00[0], LT09[10][num], color = 'green')
	ax.plot(LT00[0], LT12[10][num], color = 'blue')
	ax.plot(LT00[0], LT15[10][num], color = 'indigo')
	ax.plot(LT00[0], LT18[10][num], color = 'violet')
	ax.plot(LT00[0], LT21[10][num], color = 'gray')
box = plt.gca().get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(custom_lines, ['LT00', 'LT03', 'LT06', 'LT09', 'LT12', 'LT15', 'LT18', 'LT21'], loc='center left', bbox_to_anchor=(1, 0.5), frameon = True)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.axvline(x = datetime(2015, 3, 21, 6, 00), linestyle = 'dotted', color = 'black')
plt.xlim((LT00[0][0],LT00[0][2000]))
plt.title('FAC Contribution in the X-Direction')
plt.ylabel(r'$B \ (nT)$')
plt.xlabel('UT (HH:MM)')
plt.savefig('precursorDB/docs/EventList/SEA/ideal_ssc/SM/FAC/FAC_x.png')

#plot FAC contribution in Y direction
fig, ax = plt.subplots()
for num, item in enumerate(LT00[1]):
	ax.plot(LT00[0], LT00[11][num], color = 'red')
	ax.plot(LT00[0], LT03[11][num], color = 'orange')
	ax.plot(LT00[0], LT06[11][num], color = 'yellow')
	ax.plot(LT00[0], LT09[11][num], color = 'green')
	ax.plot(LT00[0], LT12[11][num], color = 'blue')
	ax.plot(LT00[0], LT15[11][num], color = 'indigo')
	ax.plot(LT00[0], LT18[11][num], color = 'violet')
	ax.plot(LT00[0], LT21[11][num], color = 'gray')
box = plt.gca().get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(custom_lines, ['LT00', 'LT03', 'LT06', 'LT09', 'LT12', 'LT15', 'LT18', 'LT21'], loc='center left', bbox_to_anchor=(1, 0.5), frameon = True)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.axvline(x = datetime(2015, 3, 21, 6, 00), linestyle = 'dotted', color = 'black')
plt.xlim((LT00[0][0],LT00[0][2000]))
plt.title('FAC Contribution in the Y-Direction')
plt.ylabel(r'$B \ (nT)$')
plt.xlabel('UT (HH:MM)')
plt.savefig('precursorDB/docs/EventList/SEA/ideal_ssc/SM/FAC/FAC_y.png')

#plot FAC contribution in Z direction
fig, ax = plt.subplots()
for num, item in enumerate(LT00[1]):
	ax.plot(LT00[0], LT00[12][num], color = 'red')
	ax.plot(LT00[0], LT03[12][num], color = 'orange')
	ax.plot(LT00[0], LT06[12][num], color = 'yellow')
	ax.plot(LT00[0], LT09[12][num], color = 'green')
	ax.plot(LT00[0], LT12[12][num], color = 'blue')
	ax.plot(LT00[0], LT15[12][num], color = 'indigo')
	ax.plot(LT00[0], LT18[12][num], color = 'violet')
	ax.plot(LT00[0], LT21[12][num], color = 'gray')
box = plt.gca().get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(custom_lines, ['LT00', 'LT03', 'LT06', 'LT09', 'LT12', 'LT15', 'LT18', 'LT21'], loc='center left', bbox_to_anchor=(1, 0.5), frameon = True)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.axvline(x = datetime(2015, 3, 21, 6, 00), linestyle = 'dotted', color = 'black')
plt.xlim((LT00[0][0],LT00[0][2000]))
plt.title('FAC Contribution in the Z-Direction')
plt.ylabel(r'$B \ (nT)$')
plt.xlabel('UT (HH:MM)')
plt.savefig('precursorDB/docs/EventList/SEA/ideal_ssc/SM/FAC/FAC_z.png')
