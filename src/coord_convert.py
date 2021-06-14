from glob import glob
import matplotlib.pyplot as plt; plt.ion()
import supermag
import numpy as np
from csheet_integrator_altered import gmp_timeseries
from spacepy.coordinates import Coords
from spacepy.time import Ticktock
from datetime import datetime, timedelta
import pandas as pd

#lists and arrays necessary for the script to function
bn_array = np.zeros(900)	#list of values from supermag data
bn2_array = np.zeros(900)	#list of values from integrator
by_array = np.zeros(900)	#list of by values from supermag data
by2_array = np.zeros(900)	#list of by values from integrator
bz_array = np.zeros(900)	#list of bz values from supermag data
bz2_array = np.zeros(900)	#list of bz values from integrator
seconds = list(range(900))	#list of minutes (mislabeled variable) 
by_near_event = []		#hour of activity leading up to the event
bz_near_event = []		#hour of activity leading up to the event
bn_near_event = []		#hour of activity leading up to event
diff = []			#change in by between consecutive readings in supermag data
t0 = 0				#the point at which the current sheet arrives at the Earth

#locates all txt files and compiles them into a list
files = glob('/home/richard/Desktop/research/precursorDB/data/supermag/*.txt')   

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
data = pd.read_excel('/home/richard/Desktop/research/precursorDB/docs/SSC_events.xlsx')

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
onset = t_CS + delta_t					#corrected current sheet arrival time
t0 = [i for i, time in enumerate(mags['time']) if mags['time'][i] == onset]	#time used for plotting

#generate timeseries
timeseries = gmp_timeseries(IMFdz, IMFuz, IMFdy, IMFuy, Vsw , r0 = 100, w_csheet=16)

#determine the integrator start time
integrator_time  = timedelta(seconds = (len(timeseries[:,0]) - 1) * 60)
start_time = onset - integrator_time

#turn the By and Bz values from the timeseries into a spacepy Coords object
bx = np.zeros(len(timeseries[:,0]))

i = 0		#counter variable
GSMarray = []	#components of the B vector in GSM coordinates
timelist = []	#list of datetime objects
location = []#location of magnetometer

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

#turn the timelist into a spacepy Ticktock object
#record the components of the B vector and generate the timelist
while i < len(bx):
	GSMarray.append([bx[i], timeseries[:,1][i], timeseries[:,2][i]])
	timelist.append(start_time + i * timedelta(seconds = 60))
	i += 1

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

i = 0		#reset counter variable

#compile by integrator results at 60 second resolution into array of standard length (900 items) for plotting
for num, item in enumerate(magcoords):
	by2_array[i] = magcoords[num][1]
	i += 1
		
i = 0	#reset counter variable

#compile bz integrator results at 60 second resolution into array of standard length (900 items) for plotting
for num, item in enumerate(magcoords):
	bz2_array[i] = magcoords[num][2]
	i += 1
	
i = 0	#reset counter variable

#compile integrator results at 60 second resolution into array of standard length (900 items) for plotting
for num, item in enumerate(magcoords):
	bn2_array[i] = magcoords[num][0]
	i += 1

#compile supermag data into array of standard length (900 items) for plotting
for num, item in enumerate(mags[stations[iStation]]['by']):
	by_array[num] = item

for num, item in enumerate(mags[stations[iStation]]['bz']):
	bz_array[num] = item
	
for num, item in enumerate(mags[stations[iStation]]['bx']):
	bn_array[num] = item
	
'''	
#find largest gap between consecutive readings
i = 280	#set counter variable to an appropriate range

while i < 320:
	diff.append((-mags[stations[iStation]]['by'][i+2] + 8*mags[stations[iStation]]['by'][i+1] - 8*mags[stations[iStation]]['by'][i-1] + mags[stations[iStation]]['by'][i-2])/12)
	i+=1

#find the point at which the largest jump in bz occurs and assume this is the point at which the event occurs
for j, h in enumerate(diff):
	if h == max(diff):
		t0 = j + 280
'''

#set the integrator and supermag plots so that t = 0 occurs at the point where the current sheet arrives at the Earth
offset_x = [t0[0]] * 900
offset_x2 = [len(timeseries)] * 900

#find average by and bz at time of event
i = 60	#repurpose counter variable

while i >= 0:
	by_near_event.append(by_array[t0[0] - i])
	i -= 1

i = 60	#reset counter variable

while i >= 0:
	bz_near_event.append(bz_array[t0[0] - i])
	i -= 1
	
i = 60	#reset counter variable

while i >= 0:
	bn_near_event.append(bn_array[t0[0] - i])
	i -= 1

#use the average bz leading up to the event to determine how high or low the integrator results should be plotted with respect to the supermag data
by_avg = np.average(by_near_event)
offset_y = [by_avg] * 900

bz_avg = np.average(bz_near_event)
offset_z = [bz_avg] * 900

bn_avg = np.average(bn_near_event)
offset_n = [bn_avg] * 900
#% timelist[0].month % timelist[0].day % 'station: ' % stations[iStation]
#plot supermag data vs integrator results
fig = plt.figure()
fig.suptitle('Date: {} {} {} Station: {} Geo. Lat: {} Mag. Lat: {}'.format(timelist[0].year, timelist[0].month, timelist[0].day, stations[iStation], mags[stations[iStation]]['geolat'], maglat))

plt.subplot(1, 3, 1)
integrator_result, = plt.plot([x-y for x,y in zip(seconds, offset_x2)], [x+y for x,y in zip(bn2_array, offset_n)])
magdata, = plt.plot([x-y for x,y in zip(seconds, offset_x)], bn_array)
plt.legend(handles = [integrator_result, magdata], labels = ['Biot Savart Integrator Result','SuperMAG Data'])
plt.title('N')
plt.ylabel(r'$B \ (nT)$')
plt.xlabel('time (minutes)')

plt.subplot(1, 3, 2)
integrator_result, = plt.plot([x-y for x,y in zip(seconds, offset_x2)], [x+y for x,y in zip(by2_array, offset_y)])
magdata, = plt.plot([x-y for x,y in zip(seconds, offset_x)], by_array)
plt.title('E')
plt.ylabel(r'$B \ (nT)$')
plt.xlabel('time (minutes)')

plt.subplot(1, 3, 3)
integrator_result2, = plt.plot([x-y for x,y in zip(seconds, offset_x2)], [x+y for x,y in zip(bz2_array, offset_z)])
magdata, = plt.plot([x-y for x,y in zip(seconds, offset_x)], bz_array)
plt.title('Z')
plt.ylabel(r'$B \ (nT)$')
plt.xlabel('time (minutes)')
