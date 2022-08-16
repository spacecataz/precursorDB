import numpy as np
import matplotlib.pyplot as plt
import precursorDB.src.omni as omni
from spacepy.plot import style
import matplotlib.dates as mdates

listfile = 'precursorDB/data/omni/20031115.lst'

data = omni.read_ascii(listfile)

fig = plt.figure()
fig.suptitle('{} / {} / {} Event'.format(data['time'][100].year, data['time'][100].month, data['time'][100].day))

ax1 = plt.subplot(2,1,1)
by, = plt.plot(data['time'], data['BY'])
bz, = plt.plot(data['time'], data['BZ'])
plt.legend(handles = [by,bz], labels = ['By','Bz'])

plt.ylabel(r'$B \ (nT)$')
plt.xlabel('time (minutes)')

ax2 = plt.subplot(2,1,2, sharex = ax1)
pressure, = plt.plot(data['time'], data['Flow pressure'], color = 'red')
plt.ylabel(r'$Pressure \ (nPa)$')
plt.xlabel('time (UT)')

ax3 = ax2.twinx()
ax3.grid(False)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
fig.autofmt_xdate()
symh, = plt.plot(data['time'], data['SYM/H'])
plt.legend(handles = [pressure, symh], labels = ['Flow Pressure','SYM/H'])
plt.ylabel(r'$B \ (nT)$')
style()
plt.show()
#plt.savefig('precursorDB/docs/EventList/20031115.png')