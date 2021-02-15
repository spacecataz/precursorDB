import matplotlib.pyplot as plt; plt.ion()
import matplotlib.ticker as ticker
from matplotlib.font_manager import FontProperties
import pickle as pkl
import numpy as np
from csheet_integrator import gmp_timeseries, export_timeseries, import_timeseries

xaxis = 128

#lists and arrays necessary for the script to function
bz_list = []			#list of MHD values at 10 second intervals
timelist = []			#list of datetime objects with the correct resolution
bz_array = np.empty(xaxis)	#list of bz MHD values with a standard length
bz_array[:] = np.NaN
bz2_array = np.empty(xaxis)	#list of bz integrator values with a standard length
bz2_array[:] = np.NaN
offset = [73.826 / 6] * xaxis		#difference in x-axis position between integrator and MHD results
seconds = np.array(list(np.arange(xaxis, dtype=float)))	#list of seconds for plotting
seconds[:] /= 6.0

#load pickle with MHD Result
with open('dst.pkl', 'rb') as f:
	data = pkl.load(f)

#compile northward IMF data into a dictionary
north = dict(zip(data['tNorth'], data['dstNorth']))

#take only the data which is recorded in 10 second intervals so that the resolution of the MHD results match the resolution of the integrator results
for item in data['tNorth']:
	if item.second % 10 == 0:
		timelist.append(item)
		if len(timelist) == xaxis:
			break

not_started = True
#compile all the bz values from the MHD results at 10 second intervals into a list
for t in north:
	for item in timelist:
		if t == item:
			if not_started:
				if north[t] < 0:
					not_started = False
				else:
					bz_list.append(np.NaN)
					continue
			bz_list.append(north[t])

#overwrite north list to include only the values of bz and datetime objects at 10 second intervals
north = dict(zip(timelist, bz_list))

#compile MHD results into a list of standard length (900 items) for plotting
for num, item in enumerate(bz_list):
	bz_array[num] = item

timeseries = import_timeseries('../data/saved_timeseries/mhd_ideal')
if timeseries is None:
    #Run integrator for ideal event
    timeseries = gmp_timeseries(-5, 127, 2700, dT=10, r0=100)
    export_timeseries(timeseries, '../data/saved_timeseries/mhd_ideal', False)

#Compile the results from the ideal event into a list of standard length (900 items) for plotting
for num, item in enumerate(timeseries[:,2]):
	bz2_array[num] = item

#Plot integrator vs MHD results

#ax.format_xdata = lambda x: '%1d' % int(x / 60.0)
x_min = 12
x_max = 18
integrator_result, = plt.plot([x+y for x,y in zip(seconds, offset)], bz2_array, '-')
mhd_result, = plt.plot(seconds, bz_array, '-')
plt.legend(handles = [integrator_result, mhd_result], labels = ['Biot Savart Integrator Result','MHD Result'])
plt.title('MHD vs. Integrator Results')
plt.ylabel(r'$B_z \ (nT)$')
plt.xlabel('time (m)')
ax = plt.gca()
ax.xaxis.set_major_locator(ticker.MultipleLocator(1.0))
ax.xaxis.set_minor_locator(ticker.MaxNLocator(5 * (x_max - x_min)))
ax.set_xlim(12, 18)
#plt.xticks(np.arange(600, 1201, 60.0))
#plt.xlim(600, 1080)
#plt.savefig("mhdcompare.svg")
