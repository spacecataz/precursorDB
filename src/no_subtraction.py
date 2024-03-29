import pickle
from math import floor
import numpy as np
from glob import glob
import pandas as pd
import supermag
import precursorDB.src.omni as omni
import matplotlib.pyplot as plt; plt.ion()
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from spacepy.plot import style

#locates all pkl files and compiles them into a list
files = glob('precursorDB/docs/pickles/*_timeseries.pkl')

#list files
for i, f in enumerate(files):
	print(f"#{i}\t{f}") 
	
#choose event
iFile = int(input("Which event?"))
fileName = files[iFile][-23:-15]
listfile = 'precursorDB/data/omni/'+fileName+'.lst'
omnidata = omni.read_ascii(listfile)

f_in = open(files[iFile], 'rb')
coords = pickle.load(f_in)

#locates all txt files and compiles them into a list
magfiles = glob('precursorDB/data/supermag/*.txt')   

for num, item in enumerate(magfiles):
	if str(files[iFile][-23:-15]) in magfiles[num]:
		selectedmag = magfiles[num]
		mags = supermag.SuperMag(magfiles[num])

#open event database
data = pd.read_excel('precursorDB/docs/SSC_events.xlsx')

#Find the correct event in the data file
ind = int(len(mags['time'])*5/7)
magdate = mags['time'][ind].replace(hour=0, minute=0)

for num, i in enumerate(data['Date']):
	if magdate == i:
		iFile2 = num

#retrieve satellite data from excel sheet for use in integrator
IMFdz = float(data['Bz,init (nT)'][iFile2])
IMFuz = float(data['Bz,final (nT)'][iFile2]) 
IMFdy = float(data['By,init (nT)'][iFile2])
IMFuy = float(data['By,final (nT)'][iFile2]) 
Vsw = float(data['Usw (km/s)'][iFile2]) 
t_P = datetime.combine(data['Date'][iFile2], data['t,P'][iFile2])			#time of pressure increase
t_H = datetime.combine(data['Date'][iFile2], data['t,SYM-H'][iFile2])		#time of SYM-H increase
t_CS = datetime.combine(data['Date'][iFile2], data['t,CS'][iFile2])		#time of current sheet arrival

#account for error in arrival time
delta_t = t_P - t_H					#difference between pressure increase and SYM-H increase
onset = t_CS - delta_t					#corrected current sheet arrival time
		
timelist = []	#list of datetime objects

i = 0		#reset counter variable

#record the components of the B vector and generate the timelist
while i < len(coords['SM']):
	timelist.append(t_CS - i * timedelta(seconds = 60))
	i += 1

timelist = np.flip(np.array(timelist))
stations = list(mags.keys())[1:]

#open file
f = open(selectedmag, 'r')

#create lists necessary for coordinate conversions
stationsUsed = []
lines = []
maglat = []
lt = []
N = []
E = []
Z = []

i = 0 #counter variable

#read information from SuperMAG data
while i < 64:
	f.readline()
	i+= 1

for item in f.readlines():
	if files[iFile][-23:-19] not in item:
		lines.append(item)
	else:
		break
		
for station in stations:
	for line in lines:
		if station in line:
			stationsUsed.append(station)
	
for station in stationsUsed:
	for line in lines:
		if station in line:
			maglat.append(float(line.split()[6]) * np.pi / 180)

#insert relevant data into empty lists
lat = []		
for station in stationsUsed:
	lt.append(mags[station]['lt'])
	N.append(mags[station]['bx'])
	E.append(mags[station]['by'])
	Z.append(mags[station]['bz'])
	lat.append(mags[station]['geolat'])


stationsUseda = []
maglata = []
lta = []
Na = []
Ea = []
Za = []

for num, i in enumerate(lt):
	if floor(i[305]) in range(7,17) and floor(maglat[num]*180/np.pi) in range(45,135):
		stationsUseda.append(stationsUsed[num])
		lta.append(i)
		Na.append(mags[stationsUsed[num]]['bx'])
		Ea.append(mags[stationsUsed[num]]['by'])
		Za.append(mags[stationsUsed[num]]['bz'])
		maglata.append(maglat[num])

#Create empty lists for coordinate conversions
converted_coords_x = []
converted_coords_y = []
converted_coords_z = []

#Convert coordinates
for n, item in enumerate(stationsUseda):
	for num, bx in enumerate(mags[item]['bx']):
		x = Na[n][num] * np.cos(maglata[n]) * np.cos(lta[n][num]* np.pi /12) + Za[n][num] * np.sin(maglata[n]) * np.cos(lta[n][num]*np.pi/12) + Ea[n][num] * np.sin(lta[n][num]*np.pi/12)
		y = Na[n][num] * np.cos(maglata[n]) * np.sin(lta[n][num]*np.pi / 12) + Za[n][num] * np.sin(maglata[n]) * np.sin(lta[n][num]*np.pi/12) - Ea[n][num] * np.cos(lta[n][num]*np.pi/12)
		z = Na[n][num] * np.sin(maglata[n]) - Za[n][num] * np.cos(maglata[n])
		converted_coords_x.append(x)
		converted_coords_y.append(y)
		converted_coords_z.append(z)

x_coords = [converted_coords_x[i:i+len(mags[stationsUsed[0]]['bx'])]for i in range(0,len(converted_coords_x),len(mags[stationsUsed[0]]['bx']))]
y_coords = [converted_coords_y[i:i+len(mags[stationsUsed[0]]['by'])]for i in range(0,len(converted_coords_y),len(mags[stationsUsed[0]]['by']))]
z_coords = [converted_coords_z[i:i+len(mags[stationsUsed[0]]['bz'])]for i in range(0,len(converted_coords_z),len(mags[stationsUsed[0]]['bz']))]

#find current sheet arrival time for plotting
newind = 0

for num, date in enumerate(mags['time']):
	if date == t_CS:
		newind = num
'''
#shift plots so B = 0 at t = 0
for i, item in enumerate(x_coords):
	x_coords[i] = x_coords[i] - item[newind]

for i, item in enumerate(y_coords):
	y_coords[i] = y_coords[i] - item[newind]

for i, item in enumerate(z_coords):
	z_coords[i] = z_coords[i] - item[newind]

for i, item in enumerate(coords['SM'].x):
	coords['SM'].x[i] = coords['SM'].x[i] - coords['SM'].x[-1]

for i, item in enumerate(coords['SM'].y):
	coords['SM'].y[i] = coords['SM'].y[i] - coords['SM'].y[-1]

for i, item in enumerate(coords['SM'].z):
	coords['SM'].z[i] = coords['SM'].z[i] - coords['SM'].z[-1]
'''
#Set plot color scheme
nCurves = len(stationsUseda)
NameMap = 'gist_heat'
cNorm = Normalize(vmin=0, vmax=nCurves-1) 				
cMap  = ScalarMappable(cmap=plt.get_cmap(NameMap), norm=cNorm)
style()

xlim_min = onset-timedelta(minutes=120)
xlim_max = onset+timedelta(minutes=60)

a = np.where(mags['time']==xlim_min)[0][0]
b = np.where(mags['time']==xlim_max)[0][0]
yvals=[]

#x-direction plot
fig, axs = plt.subplots(3, 1, figsize=(8,8), gridspec_kw={'height_ratios': [9,3,3]}, sharex=True)
fig.suptitle('Magnetometers, x-direction, {} / {} / {} Event'.format(onset.year, onset.month, onset.day))
for i, plot in enumerate(x_coords):
	color = cMap.to_rgba(i)
	axs[0].plot(mags['time'], plot, color = color)
	yvals.append(plot[a:b])
yvals = [item for sublist in yvals for item in sublist]
axs[0].plot(timelist, coords['SM'].x, color = 'blue', label='Integrator')
axs[0].set_ylabel(r'$B \ (nT)$')
axs[0].set_xlim((xlim_min,xlim_max))
axs[0].set_ylim((min(yvals),max(yvals)))
axs[0].legend()
axs[1].plot(omnidata['time'], omnidata['BY'], label = 'By')
axs[1].plot(omnidata['time'], omnidata['BZ'], label = 'Bz')
axs[1].set_ylabel(r'$B \ (nT)$')
axs[2].yaxis.label.set_color('blue') 
axs[1].legend(loc=2)
ax1 = axs[2].plot(omnidata['time'], omnidata['SYM/H'], color = 'blue')
ax = axs[2].twinx()
ax2 = ax.plot(omnidata['time'], omnidata['Flow pressure'], color = 'red')
ax.grid(False)
ax.set_ylabel('Pressure (nPa)')
axs[2].set_ylabel(r'$SYM/H \ (nT)$')
ax.yaxis.label.set_color('blue')
axs[2].yaxis.label.set_color('red')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
axs[2].set_xlabel('UT (HH:MM)')
plt.savefig('precursorDB/docs/EventList/SEA/EventsSummary/'+str(onset.year)+f"{onset.month:02}"+f"{onset.day:02}"+'/no_subtraction/'+fileName+'_x.png')

#y-direction plot
yvals=[]
fig, axs = plt.subplots(3, 1, figsize=(8,8), gridspec_kw={'height_ratios': [9,3,3]}, sharex=True)
fig.suptitle('Magnetometers, y-direction, {} / {} / {} Event'.format(onset.year, onset.month, onset.day))
for i, plot in enumerate(y_coords):
	color = cMap.to_rgba(i)
	axs[0].plot(mags['time'], plot, color = color)
	yvals.append(plot[a:b])
yvals = [item for sublist in yvals for item in sublist]
axs[0].plot(timelist, coords['SM'].y, color = 'blue', label='Integrator')
axs[0].set_ylabel(r'$B \ (nT)$')
axs[0].set_xlim((xlim_min,xlim_max))
axs[0].set_ylim((min(yvals),max(yvals)))
axs[0].legend()
axs[1].plot(omnidata['time'], omnidata['BY'], label = 'By')
axs[1].plot(omnidata['time'], omnidata['BZ'], label = 'Bz')
axs[1].set_ylabel(r'$B \ (nT)$')
axs[2].yaxis.label.set_color('blue') 
axs[1].legend(loc=2)
ax1 = axs[2].plot(omnidata['time'], omnidata['SYM/H'], color = 'blue')
ax = axs[2].twinx()
ax2 = ax.plot(omnidata['time'], omnidata['Flow pressure'], color = 'red')
ax.grid(False)
ax.set_ylabel('Pressure (nPa)')
axs[2].set_ylabel(r'$SYM/H \ (nT)$')
ax.yaxis.label.set_color('blue')
axs[2].yaxis.label.set_color('red')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
axs[2].set_xlabel('UT (HH:MM)')
plt.savefig('precursorDB/docs/EventList/SEA/EventsSummary/'+str(onset.year)+f"{onset.month:02}"+f"{onset.day:02}"+'/no_subtraction/'+fileName+'_y.png')

#z-direction plot
yvals=[]
fig, axs = plt.subplots(3, 1, figsize=(8,8), gridspec_kw={'height_ratios': [9,3,3]}, sharex=True)
fig.suptitle('Magnetometers, z-direction, {} / {} / {} Event'.format(onset.year, onset.month, onset.day))
for i, plot in enumerate(z_coords):
	color = cMap.to_rgba(i)
	axs[0].plot(mags['time'], plot, color = color)
	yvals.append(plot[a:b])
yvals = [item for sublist in yvals for item in sublist]
axs[0].plot(timelist, coords['SM'].z, color = 'blue', label='Integrator')
axs[0].set_ylabel(r'$B \ (nT)$')
axs[0].set_xlim((xlim_min,xlim_max))
axs[0].set_ylim((min(yvals),max(yvals)))
axs[0].legend()
axs[1].plot(omnidata['time'], omnidata['BY'], label = 'By')
axs[1].plot(omnidata['time'], omnidata['BZ'], label = 'Bz')
axs[1].set_ylabel(r'$B \ (nT)$')
axs[2].yaxis.label.set_color('blue') 
axs[1].legend(loc=2)
ax1 = axs[2].plot(omnidata['time'], omnidata['SYM/H'], color = 'blue')
ax = axs[2].twinx()
ax2 = ax.plot(omnidata['time'], omnidata['Flow pressure'], color = 'red')
ax.grid(False)
ax.set_ylabel('Pressure (nPa)')
axs[2].set_ylabel(r'$SYM/H \ (nT)$')
ax.yaxis.label.set_color('blue')
axs[2].yaxis.label.set_color('red')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
axs[2].set_xlabel('UT (HH:MM)')
plt.savefig('precursorDB/docs/EventList/SEA/EventsSummary/'+str(onset.year)+f"{onset.month:02}"+f"{onset.day:02}"+'/no_subtraction/'+fileName+'_z.png')