import matplotlib.pyplot as plt; plt.ion()
from matplotlib.font_manager import FontProperties
import numpy as np
from csheet_integrator import gmp_timeseries
import supermag
from glob import glob
import pandas as pd
from spacepy.plot import style

#lists and arrays necessary for the script to function
bz_array = np.zeros(900)	#list of bz values form supermag data
bz2_array = np.empty(900)	#list of bz values from integrator
bz2_array[:] = np.NaN
seconds = list(range(900))	#list of MINUTES (mislabeled variable) 
bz_near_event = []		#hour of activity leading up to the event
diff = []			#change in bz between consecutive readings in supermag data
t0 = 0				#the point at which the current sheet arrives at the Earth

#compile a list of all the supermag data files
files = glob('precursorDB/data/supermag/*.txt')

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

#compile and print a list of stations which were active at the time of the event chosen above
stations = list(mags.keys())[1:]
for j, g in enumerate(stations):
	print(f"#{j}\t{g}") 

#prompt the user to give which station to take data from
iStation = int(input("What station do you choose?"))
iStation
stations[iStation]

#open events excel sheet
data = pd.read_excel('precursorDB/docs/SSC_events.xlsx', engine='openpyxl')
#retrieve satellite information from excel sheet for use in integrator
IMF_d = float(data['Bz,init (nT)'][iFile])
IMF_u = float(data['Bz,final (nT)'][iFile]) 
V_sw = float(data['Usw (km/s)'][iFile])

#run integrator
timeseries = gmp_timeseries([0, 0, IMF_d], [0, 0, IMF_u], [-V_sw, 0, 0])

#compile integrator results at 60 second resolution into array of standard length (900 items) for plotting
for num, item in enumerate(timeseries[1][:,2]):
	bz2_array[num] = item
		
j = 0	#counter variable

#compile supermag data into array of standard length (900 items) for plotting
for num, item in enumerate(mags[stations[iStation]]['bx']):
	bz_array[num] = item

#find largest gap between consecutive readings
i = 0	#reset counter variable
while i+1 < len(mags[stations[iStation]]['bx']):
	diff.append(mags[stations[iStation]]['bx'][i + 1] - mags[stations[iStation]]['bx'][i])
	i += 1

#find the point at which the largest jump in bz occurs and assume this is the point at which the event occurs
for j, h in enumerate(diff):
	if h == max(diff):
		t0 = j - 1

#set the integrator and supermag plots so that t = 0 occurs at the point where the current sheet arrives at the Earth
offset_x = [t0] * 900
offset_x2 = [len(timeseries[1])] * 900

#find average bz at time of event
i = 60	#repurpose counter variable

while i >= 0:
	bz_near_event.append(bz_array[t0 - i])
	i -= 1

#use the average bz leading up to the event to determine how high or low the integrator results should be plotted with respect to the supermag data
bz_avg = np.average(bz_near_event)
offset_y = [bz_avg] * 900

#plot supermag data vs integrator results
style()
integrator_result, = plt.plot([x-y for x,y in zip(seconds, offset_x2)], [x+y for x,y in zip(bz2_array, offset_y)])
mhd_result, = plt.plot([x-y for x,y in zip(seconds, offset_x)], bz_array)
plt.legend(handles = [integrator_result, mhd_result], labels = ['Biot Savart Integrator Result','SuperMAG Data'])
plt.title('SuperMAG Data vs. Integrator Results')
plt.ylabel(r'$B_z \ (nT)$')
plt.xlabel('time (minutes)')

