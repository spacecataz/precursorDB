# -*- coding: utf-8 -*-
"""
Module that compares our Integrator results for an Ideal event to MHD results.

@authors: RL2, DSK
"""

import pickle as pkl
import numpy as np
from csheet_integrator import gmp_timeseries
from csheet_integrator import import_timeseries, export_timeseries
from plt_pdb import build_mhd_plot, export_figure


def prep_plot(seconds, offset, bz_array, bz2_array):
    """
    Prepare lists of the X and Y axes for the integrator and MHD results.

    Parameters
    ----------
    seconds : TYPE
        DESCRIPTION.
    offset : TYPE
        DESCRIPTION.
    bz_array : TYPE
        DESCRIPTION.
    bz2_array : TYPE
        DESCRIPTION.

    Returns
    -------
    integrator : TYPE
        DESCRIPTION.
    mhd : TYPE
        DESCRIPTION.

    """
    integrator = [[x + y for x, y in zip(seconds, offset)], bz2_array]
    mhd = [seconds, bz_array]
    return integrator, mhd


def compare_integrator_to_mhd(xaxis=128):
    """
    Format data from the Ideal MHD event and compare to integrator results.

    Parameters
    ----------
    xaxis : int, optional
        Number of MHD data points to process. The default is 128.

    Returns
    -------
    None.

    """
    # lists and arrays necessary for the script to function
    bz_list = []  # list of MHD values at 10 second intervals
    timelist = []  # list of datetime objects with the correct resolution

    # list of bz MHD values with a standard length
    bz_array = np.empty(xaxis)
    bz_array[:] = np.NaN

    # list of bz integrator values with a standard length
    bz2_array = np.empty(xaxis)
    bz2_array[:] = np.NaN

    # difference in x-axis position between integrator and MHD results
    offset = [73.826 / 6] * xaxis

    # list of seconds for plotting
    seconds = np.array(list(np.arange(xaxis, dtype=float)))
    seconds[:] /= 6.0

    # load pickle with MHD Result
    with open('dst.pkl', 'rb') as f:
        data = pkl.load(f)

    # compile northward IMF data into a dictionary
    north = dict(zip(data['tNorth'], data['dstNorth']))

    # only take data in 10 second intervals so the resolutions match
    for item in data['tNorth']:
        if item.second % 10 == 0:
            timelist.append(item)
            if len(timelist) == xaxis:
                break

    # create bool to track if there is actual data from the mhd run yet
    not_started = True

    # compile all bz values from MHD results at 10 second intervals
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

    # overwrite north with only the values at 10 second intervals
    north = dict(zip(timelist, bz_list))

    # compile MHD results into a standard length list (900 items) for plotting
    for num, item in enumerate(bz_list):
        bz_array[num] = item

    # attempt to import existing timeseries for the current parameters
    timeseries = import_timeseries('../data/saved_timeseries/mhd_ideal4')
    if timeseries is None:
        # no existing timeseries file found, run integrator for ideal event
        timeseries = gmp_timeseries([0, 0, -5], [0, 0, 127], [-2700, 0, 0],
                                    dT=10, r0=100, dI=0.4)
        export_timeseries(timeseries,
                          '../data/saved_timeseries/mhd_ideal4', False)

    # compile ideal event into a standard length list (900 items) for plotting
    for num, item in enumerate(timeseries[:, 2]):
        bz2_array[num] = item

    # plot integrator vs MHD results
    integ_plt, mhd_plt = prep_plot(seconds, offset, bz_array, bz2_array)

    fig = build_mhd_plot(integ_plt, mhd_plt)

    # allow setting new x limits for the plot
    new_xlims = str(input('Set new minimum and maximum x? (y/N) '))
    while new_xlims.upper() == 'Y':
        x_min = int(input('Set new min x: '))
        x_max = int(input('Set new max x: '))
        fig = build_mhd_plot(integ_plt, mhd_plt, x_min=x_min, x_max=x_max)
        new_xlims = str(input('Set new minimum and maximum x? (y/N) '))

    # check if we should export this plot to svg
    do_save = str(input('Export plot to svg file? (y/N) '))
    if do_save.upper() == 'Y':
        export_figure(fig, '__local__/exports/mhdcompare.svg')


if __name__ == '__main__':
    compare_integrator_to_mhd()
