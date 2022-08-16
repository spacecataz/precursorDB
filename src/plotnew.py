from glob import glob
import matplotlib.pyplot as plt; plt.ion()
import supermag
import precursorDB.src.omni as omni
import numpy as np
from csheet_integrator_altered import gmp_timeseries
from spacepy.plot import style
from spacepy.coordinates import Coords
from spacepy.time import Ticktock
from datetime import datetime, timedelta
import pandas as pd

#locates all txt files and compiles them into a list
files = glob('precursorDB/data/supermag/*.txt')   

#list files
for i, f in enumerate(files):
	print(f"#{i}\t{f}") 

#choose event
iFile = int(input("Which event?"))
iFile
files[iFile]

#get keys from supermag dictionary
mags = supermag.SuperMag(files[iFile])
mags.keys()

#open events excel sheet
data = pd.read_excel('precursorDB/docs/SSC_events.xlsx')

#compile a list of stations which were active at the time of the event chosen above
stations = list(mags.keys())[1:]

for j, g in enumerate(stations):
		print(f"#{j}\t{g}") 

#prompt the user to give which station to take data from
iStation = int(input("What station do you choose?"))
iStation
stations[iStation]

#open file
f = open(files[iFile], 'r')

j = 0	#reset counter variable

#skip header
while j < 2:
	skip = f.readline()
	if str('***') in skip:
		j +=1

j = 0	#reset counter variable

#find and isolate magnetic latitude and longitude
while j < 2:	#skip the first time the magnetometers are listed
	line = f.readline()
	if stations[iStation] in line:
		j += 1

maglon = float(line.split()[3])
maglat = float(line.split()[4])

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

#get omniweb data
path = 'precursorDB/data/omni/'+str(data['Date'][iFile].year)+str(data['Date'][iFile].month)+str(data['Date'][iFile].day)+'.lst'
omni = omni.read_ascii(path)

#generate timeseries
timeseries = gmp_timeseries(IMFdz, IMFuz, IMFdy, IMFuy, Vsw , r0 = 10, w_csheet=8)

#determine the integrator start time
integrator_time  = timedelta(seconds = (len(timeseries[:,0]) - 1) * 60)
start_time = onset - integrator_time

#turn the By and Bz values from the timeseries into a spacepy Coords object
bx = np.zeros(len(timeseries[:,0]))

i = 0		#counter variable
GSMarray = []	#components of the B vector in GSM coordinates
timelist = []	#list of datetime objects
location = []   #location of magnetometer

#make a location list as long as timelist
while i < len(timeseries[:,0]):
	location.append([1.0, mags[str(stations[iStation])]['geolat'], mags[str(stations[iStation])]['geolon']])
	i +=1

i = 0		#reset counter variable

#record the components of the B vector and generate the timelist
while i < len(bx):
	GSMarray.append([bx[i], timeseries[:,1][i], timeseries[:,2][i]])
	timelist.append(start_time + i * timedelta(seconds = 60))
	i += 1

#turn the B vector and the magentometer location into spacepy Coords objects
location_geo = Coords(location, 'GEO', 'sph')
GSM = Coords(GSMarray, 'GSM', 'car')
GSM.ticks = Ticktock(timelist, 'UTC')
location_geo.ticks = Ticktock(timelist, 'UTC')

#convert to SM coordinate system
middle_step = GSM.convert('GEO', 'car') #spacepy won't let me convert directly to SM coordinates for whatever reason
SM = middle_step.convert('SM', 'car')
locationSM = location_geo.convert('SM', 'car')

maglon = []	#keep track of magnetic longitude
i = 0		#reset counter variable

#find magnetic longitude
while i < len(locationSM):
     maglon.append(float(np.arctan2(locationSM[i].y, locationSM[i].x)))
     i += 1

magcoords = []  #list of magnetometer coordinates

#convert to NEZ coordinates
for num, coord in enumerate(SM.data):
	Nvec = coord[2] * np.cos(maglon[num]) - coord[0] * np.sin(maglon[num]) * np.cos(maglat * np.pi / 180) - coord[1] * np.sin(maglon[num]) * np.sin(maglat * np.pi / 180)
	Evec = coord[1] * np.cos(maglat * np.pi / 180) - coord[0] * np.sin(maglat * np.pi / 180)
	Zvec = -coord[0] * np.cos(maglon[num]) * np.cos(maglat * np.pi / 180) - coord[1] * np.sin(maglat * np.pi / 180) * np.cos(maglon[num]) - coord[2] * np.sin(maglon[num])
	magcoords.append([Nvec, Evec, Zvec])

mg = np.array(magcoords)
tl = np.array(timelist)

#plot everything
style()
fig1 = plt.figure(1)
fig1.suptitle('Date: {} {} {} Station: {} Geo. Lat: {} Mag. Lat: {}'.format(timelist[0].year, timelist[0].month, timelist[0].day, stations[iStation], mags[stations[iStation]]['geolat'], maglat))

ax1 = plt.subplot(3,1,1)
by, = plt.plot(omni['time'], omni['BY'])
bz, = plt.plot(omni['time'], omni['BZ'])
plt.legend(handles = [by,bz], labels = ['By','Bz'])
plt.title('By and Bz (OMNIWeb)')
plt.ylabel(r'$B \ (nT)$')
plt.xlabel('time (minutes)')

ax2 = plt.subplot(3,1,2, sharex = ax1)
pressure, = plt.plot(omni['time'], omni['Flow pressure'], color = 'red')
plt.title('Pressure and SYM/H (OMNIWeb)')
plt.ylabel(r'$Pressure \ (nPa)$')
plt.xlabel('time (minutes)')

ax3 = ax2.twinx()
#fig.autofmt_xdate()
symh, = plt.plot(omni['time'], omni['SYM/H'])
plt.legend(handles = [pressure, symh], labels = ['Flow Pressure','SYM/H'])
plt.ylabel(r'$B \ (nT)$')
fig1.tight_layout()

plt.subplot(3,1,3, sharex = ax1)
integrator_result, = plt.plot(tl, mg[:,0])
magdata, = plt.plot(mags['time'], mags[stations[iStation]]['bx'])
plt.legend(handles = [integrator_result, magdata], labels = ['Biot Savart Integrator Result','SuperMAG Data'])
plt.title('N')
plt.ylabel(r'$B \ (nT)$')
plt.xlabel('time (minutes)')

fig2 = plt.figure(2)
fig2.suptitle('Date: {} {} {} Station: {} Geo. Lat: {} Mag. Lat: {}'.format(timelist[0].year, timelist[0].month, timelist[0].day, stations[iStation], mags[stations[iStation]]['geolat'], maglat))

ax4 = plt.subplot(3,1,1)
integrator_result, = plt.plot(tl, mg[:,0])
magdata, = plt.plot(mags['time'], mags[stations[iStation]]['bx'])
plt.legend(handles = [integrator_result, magdata], labels = ['Biot Savart Integrator Result','SuperMAG Data'])
plt.title('N')
plt.ylabel(r'$B \ (nT)$')
plt.xlabel('time (minutes)')

plt.subplot(3, 1, 2, sharex = ax4)
integrator_result, = plt.plot(tl, mg[:,1])
magdata, = plt.plot(mags['time'], mags[stations[iStation]]['by'])
plt.title('E')
plt.ylabel(r'$B \ (nT)$')
plt.xlabel('time (minutes)')

plt.subplot(3, 1, 3, sharex = ax4)
integrator_result2, = plt.plot(tl, mg[:,2])
magdata, = plt.plot(mags['time'], mags[stations[iStation]]['bz'])
plt.title('Z')
plt.ylabel(r'$B \ (nT)$')
plt.xlabel('time (minutes)')
fig2.tight_layout()
