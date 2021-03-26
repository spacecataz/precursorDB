from datetime import datetime, timedelta
import matplotlib.pyplot as plt; plt.ion()
from matplotlib.font_manager import FontProperties
import numpy as np
from csheet_integrator_altered import gmp_timeseries
import supermag
from glob import glob
import pandas as pd

#lists and arrays necessary for the script to function
by_array = np.zeros(900)	#list of by values from supermag data
by2_array = np.zeros(900)	#list of by values from integrator
bz_array = np.zeros(900)	#list of bz values from supermag data
bz2_array = np.zeros(900)	#list of bz values from integrator
seconds = list(range(900))	#list of minutes (mislabeled variable) 
by_near_event = []		#hour of activity leading up to the event
bz_near_event = []		#hour of activity leading up to the event
diff = []			#change in by between consecutive readings in supermag data
t0 = 0				#the point at which the current sheet arrives at the Earth

#compile a list of all the supermag data files
files = glob('/home/richard/Desktop/research/precursorDB/data/supermag/*.txt')  

#print the supermag data files
for i, f in enumerate(files):
	print(f"#{i}\t{f}")

#prompt the user to give which supermag file to analyze
iFile = int(input("What file do you choose?"))
iFile
files[iFile]

#get keys from supermag dictionary
mags = supermag.SuperMag(files[iFile])
mags.keys()

#compile a list of stations which were active at the time of the event chosen above
stations = list(mags.keys())[1:]

#determine the time of the event (GMT)
start_time = mags['time'][0]
GMT = start_time + timedelta(hours = 5)

#read longitude of stations
stat_info = supermag.read_statinfo()
counter = 0
longitudes = []
while counter < len(stations):
	longitudes.append(stat_info[stations[counter]]['geolon'])
	counter += 1

#for each magentometer in stations list, determine the time of the event at the station
counter = 0
mg_time = []
while counter < len(stations):
	mg_time.append(GMT + timedelta(hours = (longitudes[counter] / 360) * 24))
	counter += 1

#creates a dictionary that maps magnetometers to their respective times
mag_time_dict = dict(zip(stations, mg_time))

#checks which magnetometers are on the dayside and lists them
counter = 0
dayside = []
while counter < len(stations):
	if 9 <= mg_time[counter].hour < 15:
		dayside.append(stations[counter])
	counter += 1
else:
	for j, g in enumerate(dayside):
		print(f"#{j}\t{g}") 

#prompt the user to give which station to take data from
iStation = int(input("What station do you choose?"))
iStation
dayside[iStation]

#open events excel sheet
data = pd.read_excel('/home/richard/Desktop/research/precursorDB/docs/SSC_events.xlsx')

#retrieve satellite information from excel sheet for use in integrator
IMFdy = float(data['By,init (nT)'][iFile])
IMFuy = float(data['By,final (nT)'][iFile])
IMFdz = float(data['Bz,init (nT)'][iFile])
IMFuz = float(data['Bz,final (nT)'][iFile]) 
Vsw = float(data['Usw (km/s)'][iFile]) 

#run integrator
timeseries = gmp_timeseries(IMFdz, IMFuz, IMFdy, IMFuy, Vsw)

i = 0	#counter variable

#compile by integrator results at 60 second resolution into array of standard length (900 items) for plotting
for num, item in enumerate(timeseries[:,1]):
	by2_array[i] = timeseries[num][1]
	i += 1
		
i = 0	#reset counter variable

#compile bz integrator results at 60 second resolution into array of standard length (900 items) for plotting
for num, item in enumerate(timeseries[:,2]):
	bz2_array[i] = timeseries[num][2]
	i += 1

#compile supermag data into array of standard length (900 items) for plotting
for num, item in enumerate(mags[dayside[iStation]]['by']):
	by_array[num] = item

for num, item in enumerate(mags[dayside[iStation]]['bx']):
	bz_array[num] = item
	
#find largest gap between consecutive readings
i = 280	#set counter variable to an appropriate range

while i < 320:
	diff.append((-mags[dayside[iStation]]['by'][i+2] + 8*mags[dayside[iStation]]['by'][i+1] - 8*mags[dayside[iStation]]['by'][i-1] + mags[dayside[iStation]]['by'][i-2])/12)
	i+=1

#find the point at which the largest jump in bz occurs and assume this is the point at which the event occurs
for j, h in enumerate(diff):
	if h == max(diff):
		t0 = j + 280

#set the integrator and supermag plots so that t = 0 occurs at the point where the current sheet arrives at the Earth
offset_x = [t0] * 900
offset_x2 = [len(timeseries)] * 900

#find average by and bz at time of event
i = 60	#repurpose counter variable

while i >= 0:
	by_near_event.append(by_array[t0 - i])
	i -= 1

i = 60	#reset counter variable

while i >= 0:
	bz_near_event.append(bz_array[t0 - i])
	i -= 1

#use the average bz leading up to the event to determine how high or low the integrator results should be plotted with respect to the supermag data
by_avg = np.average(by_near_event)
offset_y = [by_avg] * 900

bz_avg = np.average(bz_near_event)
offset_z = [bz_avg] * 900

#plot supermag data vs integrator results
plt.subplot(1, 2, 1)
integrator_result, = plt.plot([x-y for x,y in zip(seconds, offset_x2)], [x+y for x,y in zip(by2_array, offset_y)])
mhd_result, = plt.plot([x-y for x,y in zip(seconds, offset_x)], by_array)
plt.legend(handles = [integrator_result, mhd_result], labels = ['Biot Savart Integrator Result','SuperMAG Data'])
plt.title('By')
plt.ylabel(r'$B_y \ (nT)$')
plt.xlabel('time (minutes)')

plt.subplot(1, 2, 2)
integrator_result2, = plt.plot([x-y for x,y in zip(seconds, offset_x2)], [x+y for x,y in zip(bz2_array, offset_z)])
mhd_result2, = plt.plot([x-y for x,y in zip(seconds, offset_x)], bz_array)
plt.legend(handles = [integrator_result2, mhd_result2], labels = ['Biot Savart Integrator Result','SuperMAG Data'])
plt.title('Bz')
plt.ylabel(r'$B_z \ (nT)$')
plt.xlabel('time (minutes)')

