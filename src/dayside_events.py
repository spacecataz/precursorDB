'''
-read time SSC occurred (GMT)✓
	-time of SSC is start time of event file + 5 hours✓
-read longitude from stat_info✓
-create list of longitudes for magnetometers✓
-determine time at megnetometer when event occurred✓
	-time = ((longitude / 360) * 24) + GMT✓
	-put magnetometer times into a list✓
-crete a dictionary that maps magnetometers to their respective times✓
-check to see which magnetometers are on the day side✓
'''

from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import supermag
from glob import glob

#locates all txt files and compiles them into a list
files = glob('precursorDB/data/supermag/*.txt')  

#lists files
for i, f in enumerate(files):
	print(f"#{i}\t{f}") 

#choose file
iFile = int(input("What file do you choose?"))
iFile
files[iFile]

#creates a dictionary from the selected file and retrieves the keys from that dictionary
mags = supermag.SuperMag(files[iFile])
mags.keys()

#creates and prints a list of stations
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

#checks which magnetometers are on the dayside
counter = 0
dayside = []
while counter < len(stations):
	if 8 <= mg_time[counter].hour < 16:
		dayside.append(stations[counter])
	counter += 1
else:
	print(dayside)
