import pickle
import supermag
import pandas as pd
import numpy as np
from glob import glob
from datetime import datetime, timedelta
from csheet_integrator_altered import gmp_timeseries
from spacepy.coordinates import Coords
from spacepy.time import Ticktock

timelist = []

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

#retrieve satellite data from excel sheet for use in integrator
IMFdz = float(data['Bz,init (nT)'][iFile])
IMFuz = float(data['Bz,final (nT)'][iFile]) 
IMFdy = float(data['By,init (nT)'][iFile])
IMFuy = float(data['By,final (nT)'][iFile]) 
Vsw = float(data['Usw (km/s)'][iFile]) 
day = data['Date'][iFile].day
month = data['Date'][iFile].month
year = data['Date'][iFile].year

#onset = datetime.combine(data['Date'][iFile], data['Time'][iFile])
t_P = datetime.combine(data['Date'][iFile], data['t,P'][iFile])			#time of pressure increase
t_H = datetime.combine(data['Date'][iFile], data['t,SYM-H'][iFile])		#time of SYM-H increase
t_CS = datetime.combine(data['Date'][iFile], data['t,CS'][iFile])		#time of current sheet arrival

#account for error in arrival time
delta_t = t_P - t_H					#difference between pressure increase and SYM-H increase
onset = t_CS + delta_t					#corrected current sheet arrival time
t0 = [i for i, time in enumerate(mags['time']) if mags['time'][i] == onset]	#time used for plotting

#generate timeseries
timeseries = gmp_timeseries(IMFdz, IMFuz, IMFdy, IMFuy, Vsw , r0 = 250, w_csheet=128)

#determine the integrator start time
integrator_time  = timedelta(seconds = (len(timeseries[:,0]) - 1) * 60)
start_time = onset - integrator_time

i = 0		#reset counter variable

#turn the By and Bz values from the timeseries into a spacepy Coords object
bx = np.zeros(len(timeseries[:,0]))
GSMarray = []

#record the components of the B vector and generate the timelist
while i < len(timeseries):
	GSMarray.append([bx[i], timeseries[:,1][i], timeseries[:,2][i]])
	timelist.append(start_time + i * timedelta(seconds = 60))
	i += 1

#turn GSM B-values into a spacepy Coords object
GSM = Coords(GSMarray, 'GSM', 'car')
GSM.ticks = Ticktock(timelist, 'UTC')

#convert GSM to SM
SM = GSM.convert('SM', 'car')

#save GSM and SM coordinates to dictionary
coordDict = {'GSM':GSM, 'SM':SM}

#save coordinates as pickle
f_out = open(str(year)+str(month)+str(day)+'_timeseries.pkl','wb')
pickle.dump(coordDict, f_out)
f_out.close()

