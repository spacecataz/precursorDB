#!/usr/bin/env python

'''
This stand-alone script plots the virtual satellite time series from
the Space Weather Modeling Framework simulations of the extreme storm
sudden commencement.

The resulting figure illustrates that the satellites do not see the
precursor magnetic perturbation signature.

This script requires the **SpacePy** software package:
https://github.com/spacepy/spacepy

Running This Script:
-------------------

Run from the src directory within the repository.
Use the "run" magic command within IPython.

>>> ipython3
>>> run plot_swmf_sats.py

'''

from glob import glob
import datetime as dt

import numpy as np
import matplotlib.pyplot as plt
from spacepy.pybats import bats
from spacepy.plot import style

################################
# PARAMETERS
################################

# Set arrival time for when CME contacts bow shock:
arrival = dt.datetime(2015,3,21,6,0,40)

# Turn on spacepy's "style" to get fancy plots.
style()

# Path to data that will be plotted.
path = '../data/sim_results/ssi_south/'

# X-axis limits on plot (seconds)
tmag_diff = [-60, 120]

################################
# HELPER FUNCTIONS
################################

def diff_formatter(x, pos):
    '''
    An axis label formatter for +/- time from an epoch.
    '''
    
    mins = int(np.floor(x/3600.))
    secs = np.abs(int(x - 60*mins))

    return( '{0:01d}:{1:02d}'.format(mins, secs))

def applyDiffTicks(ax, trng, dTick=60, show_ticks=True,
                   label=r'$T-T_{Arrival}$ (MM:SS)'):
    '''
    For a time range, *trng*, that is the difference from a certain
    epoch in seconds (negative and positive seconds), set x-axis 
    ticks: the limit, the locator, tick labels and axis labels.
    '''

    from matplotlib.ticker import MultipleLocator, FuncFormatter
    
    ax.set_xlim(trng)
    ax.xaxis.set_major_locator(MultipleLocator(dTick))
    ax.xaxis.set_major_formatter(FuncFormatter(diff_formatter))
    ax.set_xlabel(label, size=20)

    if not show_ticks:
        ax.set_xticklabels('')

def calc_tdiff(t1, arrival=arrival):
    t_out = np.array([(t1[i]-arrival).total_seconds() for i in range(t1.size)])
    return t_out

################################
# MAIN SCRIPT
################################

# Open all files, stash them into a list:
sats = []
for f in glob(path+'sat*.sat'): # Loop over all files in directory.
    # Load file, stash it into the satellite file.
    sats.append(bats.VirtSat(f))
    # Create an alternative time value relative to the time when
    # the shock wave hits the bow shock:
    
# Create a beautiful plot:
fig = plt.figure(figsize=[8.25,5.75])
ax  = fig.add_subplot(111)

# Plot each virtual satellite result:
for s in sats:
    # Convert time into time from impact on magnetosphere:
    t_now = calc_tdiff(s['time'])
    # Add line to plot:
    ax.plot(t_now, s['b1z'], label=f'{s["x"][0]:.1f} $R_E$', lw=2)

# Add two vertical lines to mark shock arrival into
# MHD simulation box and arrival at magpause:
ylim = ax.get_ylim()
ax.vlines( [-40, 0], ylim[0], ylim[1], linestyles='dashed')
ax.set_ylim(ylim)  # vlines changes our y range, change it back.

# Customize axis:
applyDiffTicks(ax, tmag_diff)  # Use relative time axis labels.
ax.legend(loc='lower right', ncol=2, title='Sat Location (X$_{GSM}$)')
ax.set_ylabel(r'$\Delta B_{Z}$ ($nT$)') 
ax.set_title(r'Precursor $\Delta B$: Virtual Satellites')

# Tighten up the margins:
fig.tight_layout()
