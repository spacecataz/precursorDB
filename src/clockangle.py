import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

listfile = '/home/richard/Desktop/research/precursorDB/data/omni/OMNI_FILE.lst'

data = np.genfromtxt(listfile)
data[data == 9999.99] = np.nan

clockangle = np.arctan(data[:,4], data[:,5])

date = []

for i, item in enumerate(data):
	year = int(data[:,0][i])
	doy = int(data[:,1][i])
	hour = int(data[:,2][i])
	minute = int(data[:,3][i])
	date.append(datetime(year, 1, 1) + timedelta(days = doy - 1, hours = hour, minutes = minute))

diff = []

for num, angle in enumerate(clockangle):
	diff.append(clockangle[num]-clockangle[num-1])
	
magnitude = [abs(value) for value in diff]

for num, item in enumerate(magnitude):
	if item > 2.9:
		print(date[num])

plot = plt.plot(date, diff)
plt.show()
