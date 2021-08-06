import pickle
from math import floor
import numpy as np
from glob import glob
import pandas as pd
import supermag
import matplotlib.pyplot as plt; plt.ion()
from datetime import datetime, timedelta
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

#locates all pkl files and compiles them into a list
files = glob('/home/richard/Desktop/research/precursorDB/src/*_timeseries.pkl')  

#list files
for i, f in enumerate(files):
	print(f"#{i}\t{f}") 
	
#choose event
iFile = int(input("Which event?"))
iFile
files[iFile]

f_in = open(files[iFile], 'rb')
coords = pickle.load(f_in)

#locates all txt files and compiles them into a list
magfiles = glob('/home/richard/Desktop/research/precursorDB/data/supermag/*.txt')   

for num, item in enumerate(magfiles):
	if str(files[iFile][-23:-15]) in magfiles[num]:
		selectedmag = magfiles[num]
		mags = supermag.SuperMag(magfiles[num])
		
data = pd.read_excel('/home/richard/Desktop/research/precursorDB/docs/SSC_events.xlsx')

#retrieve satellite data from excel sheet for use in integrator
IMFdz = float(data['Bz,init (nT)'][iFile])
IMFuz = float(data['Bz,final (nT)'][iFile]) 
IMFdy = float(data['By,init (nT)'][iFile])
IMFuy = float(data['By,final (nT)'][iFile]) 
Vsw = float(data['Usw (km/s)'][iFile]) 
#onset = datetime.combine(data['Date'][iFile], data['Time'][iFile])
t_P = datetime.combine(data['Date'][iFile], data['t,P'][iFile])			#time of pressure increase
t_H = datetime.combine(data['Date'][iFile], data['t,SYM-H'][iFile])		#time of SYM-H increase
t_CS = datetime.combine(data['Date'][iFile], data['t,CS'][iFile])		#time of current sheet arrival

#account for error in arrival time
delta_t = t_P - t_H					#difference between pressure increase and SYM-H increase
onset = t_CS - delta_t					#corrected current sheet arrival time
		
timelist = []	#list of datetime objects

i = 0		#reset counter variable

#record the components of the B vector and generate the timelist
while i < len(coords['SM']):
	timelist.append(onset - i * timedelta(seconds = 60))
	i += 1

timelist = np.flip(np.array(timelist))
stations = list(mags.keys())[1:]

#open file
f = open(selectedmag, 'r')

stationsUsed = []
lines = []
maglat = []
lt = []
N = []
E = []
Z = []
i=0

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
'''
statlen = floor(len(stationsUsed) / 2)

stationsUseda = [stationsUsed[i:i+statlen]for i in range(0,len(stationsUsed),statlen)]
'''
	
for station in stationsUsed:
	for line in lines:
		if station in line:
			maglat.append(float(line.split()[6]) * np.pi / 180)
	
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

converted_coords_x = []
converted_coords_y = []
converted_coords_z = []

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

nCurves = len(stationsUseda)
NameMap = 'copper'
cNorm = Normalize(vmin=0, vmax=nCurves-1) 				
cMap  = ScalarMappable(cmap=plt.get_cmap(NameMap), norm=cNorm)

fig1 = plt.figure()
for i, plot in enumerate(x_coords):
	color = cMap.to_rgba(i)
	plot1, = plt.plot(mags['time'], plot, color = color)
plot1a, = plt.plot(timelist, coords['SM'].x, color = 'red')
plt.legend(handles = [plot1a], labels = ['Biot Savart Integrator Result'])
plt.title('X in SM Coordinates for All Active Magnetometers on the Dayside Between Magnetic Colatitudes 45 and 135 During the 2000/04/06 Event')
plt.ylabel(r'$B \ (nT)$')
plt.xlabel('time (minutes)')
	
fig2 = plt.figure()
for i, plot in enumerate(y_coords):
	color = cMap.to_rgba(i)
	plot2, = plt.plot(mags['time'], plot, color = color)
plot2a, = plt.plot(timelist, coords['SM'].y, color = 'red')
plt.legend(handles = [plot2a], labels = ['Biot Savart Integrator Result'])
plt.title('Y in SM Coordinates for All Active Magnetometers on the Dayside Between Magnetic Colatitudes 45 and 135 During the 2000/04/06 Event')
plt.ylabel(r'$B \ (nT)$')
plt.xlabel('time (minutes)')

fig3 = plt.figure()
for i, plot in enumerate(z_coords):
	color = cMap.to_rgba(i)
	plot3, = plt.plot(mags['time'], plot, color = color)
plot3a, = plt.plot(timelist, coords['SM'].z, color = 'red')
plt.legend(handles = [plot3a], labels = ['Biot Savart Integrator Result'])
plt.title('Z in SM Coordinates for All Active Magnetometers on the Dayside Between Magnetic Colatitudes 45 and 135 During the 2000/04/06 Event')
plt.ylabel(r'$B \ (nT)$')
plt.xlabel('time (minutes)')
