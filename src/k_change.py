'''
-load mhd results
-map mhd results to list
-load integrator for Kw = 2
-map integrator results for Kw = 2 to list
-double Kw and repeat last 2 steps
-stop at Kw = 1024
-plot all integrator results vs mhd
'''

import matplotlib.pyplot as plt; plt.ion()
from matplotlib.font_manager import FontProperties
import pickle as pkl
import numpy as np
from csheet_integrator import gmp_timeseries

#lists and arrays necessary for the script to function
diff = []			#list of differences between consecutive MHD values
bz_neutral = []		#list of the base line bz values at the beginning of the MHD data
bz_list = []			#list of MHD values at 10 second intervals
timelist = []			#list of datetime objects with the correct resolution
bz_array = np.zeros(900)	#list of bz MHD values with a standard length
bz2_array = np.zeros(900)	#list of bz integrator values with a standard length
bz4_array = np.zeros(900)	#list of bz integrator values with a standard length
bz8_array = np.zeros(900)	#list of bz integrator values with a standard length
bz16_array = np.zeros(900)	#list of bz integrator values with a standard length
bz32_array = np.zeros(900)	#list of bz integrator values with a standard length
bz64_array = np.zeros(900)	#list of bz integrator values with a standard length
bz128_array = np.zeros(900)	#list of bz integrator values with a standard length
bz256_array = np.zeros(900)	#list of bz integrator values with a standard length
bz512_array = np.zeros(900)	#list of bz integrator values with a standard length
bz1024_array = np.zeros(900)	#list of bz integrator values with a standard length
seconds = list(range(900))	#list of seconds for plotting
j = 0				#counter variable

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
	
#find largest gap between consecutive readings
i = 0	#reset counter variable
while i+1 < len(bz_array):
	diff.append(bz_array[i + 1] - bz_array[i])
	i += 1

#find the point at which the largest jump in bz occurs and assume this is the point at which the event occurs
for j, h in enumerate(diff):
	if h == max(diff):
		t0 = j + 1

#find average bz at time of event
i = 10	#repurpose counter variable
while i >= 0:
	bz_neutral.append(bz_array[i])
	i -= 1

#use the average bz leading up to the event to determine how high or low the integrator results should be plotted with respect to the supermag data
bz_avg = np.average(bz_neutral)
offset_y = [bz_avg] * 900

#Run integrator for ideal event
timeseries2 = gmp_timeseries(-5, 127, 2700, dT = 10, w_csheet = 2)

#Compile the results from the ideal event into a list of standard length (900 items) for plotting
for num, item in enumerate(timeseries2[:,2]):
	bz2_array[num] = item
	
#set the integrator and mhd plots so that t = 0 occurs at the point where the current sheet arrives at the Earth
offset_x = [t0] * 900
offset_x2 = [len(timeseries2)] * 900

#Repeat previous steps for 4 RE current sheet
#Run integrator for ideal event and put results into list
timeseries4 = gmp_timeseries(-5, 127, 2700, dT = 10, w_csheet = 4)
for num, item in enumerate(timeseries4[:,2]):
	bz4_array[num] = item
	
#Repeat previous steps for 8 RE current sheet
#Run integrator for ideal event and put results into list
timeseries8 = gmp_timeseries(-5, 127, 2700, dT = 10, w_csheet = 8)
for num, item in enumerate(timeseries8[:,2]):
	bz8_array[num] = item
	
#Repeat previous steps for 16 RE current sheet
#Run integrator for ideal event and put results into list
timeseries16 = gmp_timeseries(-5, 127, 2700, dT = 10, w_csheet = 16)
for num, item in enumerate(timeseries16[:,2]):
	bz16_array[num] = item

#Repeat previous steps for 32 RE current sheet
#Run integrator for ideal event and put results into list
timeseries32 = gmp_timeseries(-5, 127, 2700, dT = 10, w_csheet = 32)
for num, item in enumerate(timeseries32[:,2]):
	bz32_array[num] = item
	
#Repeat previous steps for 64 RE current sheet
#Run integrator for ideal event and put results into list
timeseries64 = gmp_timeseries(-5, 127, 2700, dT = 10, w_csheet = 64)
for num, item in enumerate(timeseries64[:,2]):
	bz64_array[num] = item

#Repeat previous steps for 128 RE current sheet
#Run integrator for ideal event and put results into list
timeseries128 = gmp_timeseries(-5, 127, 2700, dT = 10, w_csheet = 128)
for num, item in enumerate(timeseries128[:,2]):
	bz128_array[num] = item

#Repeat previous steps for 256 RE current sheet
#Run integrator for ideal event and put results into list
timeseries256 = gmp_timeseries(-5, 127, 2700, dT = 10, w_csheet = 256)
for num, item in enumerate(timeseries256[:,2]):
	bz256_array[num] = item

#Repeat previous steps for 512 RE current sheet
#Run integrator for ideal event and put results into list
timeseries512 = gmp_timeseries(-5, 127, 2700, dT = 10, w_csheet = 512)
for num, item in enumerate(timeseries512[:,2]):
	bz512_array[num] = item
	
#Plot integrator vs MHD results
integrator_result2, = plt.plot([x-y for x,y in zip(seconds, offset_x2)], [x+y for x,y in zip(bz2_array, offset_y)])
integrator_result4, = plt.plot([x-y for x,y in zip(seconds, offset_x2)], [x+y for x,y in zip(bz4_array, offset_y)])
integrator_result8, = plt.plot([x-y for x,y in zip(seconds, offset_x2)], [x+y for x,y in zip(bz8_array, offset_y)])
integrator_result16, = plt.plot([x-y for x,y in zip(seconds, offset_x2)], [x+y for x,y in zip(bz16_array, offset_y)])
integrator_result32, = plt.plot([x-y for x,y in zip(seconds, offset_x2)], [x+y for x,y in zip(bz32_array, offset_y)])
integrator_result64, = plt.plot([x-y for x,y in zip(seconds, offset_x2)], [x+y for x,y in zip(bz64_array, offset_y)])
integrator_result128, = plt.plot([x-y for x,y in zip(seconds, offset_x2)], [x+y for x,y in zip(bz128_array, offset_y)])
integrator_result256, = plt.plot([x-y for x,y in zip(seconds, offset_x2)], [x+y for x,y in zip(bz256_array, offset_y)])
integrator_result512, = plt.plot([x-y for x,y in zip(seconds, offset_x2)], [x+y for x,y in zip(bz512_array, offset_y)])
mhd_result, = plt.plot([x-y for x,y in zip(seconds, offset_x)], bz_array)
plt.legend(handles = [integrator_result2, integrator_result4, integrator_result8, integrator_result16, integrator_result32, integrator_result64, integrator_result128, integrator_result256, integrator_result512, mhd_result], labels = ['2 RE Current Sheet', '4 RE Current Sheet', '8 RE Current Sheet', '16 RE Current Sheet', '32 RE Current Sheet', '64 RE Current Sheet', '128 RE Current Sheet', '256 RE Current Sheet', '512 RE Current Sheet', 'MHD Result'])
plt.title('MHD vs. Integrator Results')
plt.ylabel(r'$B_z \ (nT)$')
plt.xlabel('time (das)')
