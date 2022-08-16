import matplotlib.pyplot as plt; plt.ion()
import matplotlib.dates as mdates
from matplotlib.font_manager import FontProperties
import pickle as pkl
import numpy as np
from datetime import datetime, timedelta
from spacepy.pybats import bats
from spacepy.plot import style
from csheet_integrator import gmp_timeseries

#Run integrator for dayside and nightside magnetometers (separated by 2 RE)
timeseries_day = gmp_timeseries([0,0,-5], [0,0,-127], [-2700,0,0], dT = 10, r0 = 32, w_csheet = 256)[1][:,2]
timeseries_night = gmp_timeseries([0,0,-5], [0,0,-127], [-2700,0,0], dT = 10, r0 = 34, w_csheet = 256)[1][:,2]


onset = datetime(2015, 3, 21, 6, 0, 10)
onset2 = datetime(2015, 3, 21, 6, 0, 0)

i = 0
time = []

while len(time) < len(timeseries_day):
	time.append(onset+timedelta(seconds=i))
	i += 10

def component(filename):
	LT = int(filename[-11:-9])
	maglat = 10
	mag = bats.MagFile(filename)
	t = mag['time']
	plotlen = len(mag['time'])
	mhd = []

	#convert MHD to SM
	maglat = 10
	mhd.append(mag['d'+str(maglat)]['dBnMhd'] * np.sin((np.pi/2)-(maglat * np.pi / 180)) - mag['d'+str(maglat)]['dBdMhd'] * np.cos((np.pi/2)-(maglat * np.pi / 180)))
	
	#mhd = np.array_split(mhd, len(mhd)/plotlen)

	return t, mhd

LT00 = component('MHD/LT_00_mags.mag')
#LT03 = component('MHD/LT_03_mags.mag')
#LT06 = component('MHD/LT_06_mags.mag')
#LT09 = component('MHD/LT_09_mags.mag')
LT12 = component('MHD/LT_12_mags.mag')
#LT15 = component('MHD/LT_15_mags.mag')
#LT18 = component('MHD/LT_18_mags.mag')
#LT21 = component('MHD/LT_21_mags.mag')

time_fixed = [(x-onset2).total_seconds() for x in LT00[0]]
int_time_fixed = [(x-onset2).total_seconds() for x in time]

#plot MHD contribution in Z direction
style()
fig, ax = plt.subplots()
for num, item in enumerate(LT00[1]):
	plot1, = ax.plot(time_fixed, LT00[1][0], color = '#8800ff')
	#plot2, = plt.plot(LT03[0], LT03[1][0], color = 'orange')
	#plot3, = plt.plot(LT06[0], LT06[1][0], color = 'yellow')
	#plot4, = plt.plot(LT09[0], LT09[1][0], color = 'green')
	plot5, = ax.plot(time_fixed, LT12[1][0], color = '#0000ff')
	#plot6, = plt.plot(LT15[0], LT15[1][0], color = 'indigo')
	#plot7, = plt.plot(LT18[0], LT18[1][0], color = 'purple')
	#plot8, = plt.plot(LT21[0], LT21[1][0], color = 'gray')
integrator_day, = plt.plot(int_time_fixed, timeseries_day, color = '#0088ff')
integrator_night, = plt.plot(int_time_fixed, timeseries_night, color = '#00ffff')
ax.legend([plot1, plot5, integrator_day, integrator_night], ['Dayside Equatorial Magnetometer', 'Nightside Equatorial Magnetometer', 'Expected Dayside Precursor', 'Expected Nightside Precursor'])

#plt.xlim((LT00[0][0],LT00[0][2000]))
#plt.xticks(rotation = 45)
plt.title('MHD vs Integrator')
plt.ylabel(r'$B \ (nT)$')
plt.xlabel('Seconds from Current Sheet Entrance')
plt.show()