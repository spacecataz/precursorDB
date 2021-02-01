import matplotlib.pyplot as plt; plt.ion()
from matplotlib.font_manager import FontProperties
import pickle as pkl
import numpy as np
from csheet_integrator import gmp_timeseries

#lists and arrays necessary for the script to function
bz_list = []			#list of MHD values at 10 second intervals
timelist = []			#list of datetime objects with the correct resolution
bz_array = np.zeros(900)	#list of bz MHD values with a standard length
bz2_array = np.zeros(900)	#list of bz integrator values with a standard length
offset = [73.826] * 900		#difference in x-axis position between integrator and MHD results
seconds = list(range(900))	#list of seconds for plotting

#load pickle with MHD Result
with open('dst.pkl', 'rb') as f:
	data = pkl.load(f)

#compile northward IMF data into a dictionary
north = dict(zip(data['tNorth'], data['dstNorth']))

#take only the data which is recorded in 10 second intervals so that the resolution of the MHD results match the resolution of the integrator results
for item in data['tNorth']:
	if item.second % 10 == 0:
		timelist.append(item)

#compile all the bz values from the MHD results at 10 second intervals into a list
for t in north:
	for item in timelist:
		if t == item:
			bz_list.append(north[t])

#overwrite north list to include only the values of bz and datetime objects at 10 second intervals
north = dict(zip(timelist, bz_list))

#compile MHD results into a list of standard length (900 items) for plotting
for num, item in enumerate(bz_list):
	bz_array[num] = item

#Run integrator for ideal event
timeseries = gmp_timeseries(-5, 127, 2700, dT = 10)

#Compile the results from the ideal event into a list of standard length (900 items) for plotting
for num, item in enumerate(timeseries[:,2]):
	bz2_array[num] = item

#Plot integrator vs MHD results
integrator_result, = plt.plot([x+y for x,y in zip(seconds, offset)], bz2_array)
mhd_result, = plt.plot(seconds, bz_array)
plt.legend(handles = [integrator_result, mhd_result], labels = ['Biot Savart Integrator Result','MHD Result'])
plt.title('MHD vs. Integrator Results')
plt.ylabel(r'$B_z \ (nT)$')
plt.xlabel('time (min)')
