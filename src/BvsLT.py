import matplotlib.pyplot as plt
from spacepy.pybats import bats
from datetime import datetime
from glob import glob
import matplotlib.dates as mdates
import numpy as np
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from spacepy.plot import style; style()

loc = 'SWMF/run_test/GM/IO2/'
savloc = 'test4/'

files = glob(loc + 'mag_grid*.out')
files.sort(key = str)

nCurves = 86
colors = []
NameMap = 'gist_heat'
cNorm = Normalize(vmin=0, vmax=nCurves-1)
cMap  = ScalarMappable(cmap=plt.get_cmap(NameMap), norm=cNorm)

for num in range(86):
    colors.append(cMap.to_rgba(num))

def mags(filename):
    mags = bats.MagGridFile(filename)
    fig, ax = plt.subplots(figsize=(6,5))
    ax.set_prop_cycle(color = colors)
    plt.plot(mags['Lon'], mags['dBnMhd'])
    box = plt.gca().get_position()
    cbar = fig.colorbar(ScalarMappable(norm=cNorm, cmap=NameMap), ticks=[0,17,34,51,68,85], ax=ax, label='Latitude')
    cbar.ax.set_yticklabels(['0', '17', '34', '51', '68', '85'])
    plt.title(r'$B_n \ vs. \ LT$')
    plt.ylabel(r'$B_n \ (nT)$')
    plt.xticks(ticks = [0, 45, 90, 135, 180, 225, 270, 315, 360], labels = ['12', '15', '18', '21', '00', '03', '06', '09', '12'])
    plt.xlabel('Local Time')
    plt.tight_layout()
    plt.savefig(savloc+filename[-10:-4]+'.png', bbox_inches='tight')
    plt.close()
    return mags

for file in files[920:1800]:
    mags(file)
'''
test = mags(files[1080])
'''