# -*- coding: utf-8 -*-
"""
Module that assists in standard formatting of our plots.

Created on Mon Mar 29 10:11:26 2021

@author: DSK
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from os.path import isdir
from os import makedirs


def build_mhd_plot(*args, x_min=None, x_max=None):
    """
    Build and display a plot for preview comparing integrator to mhd results.

    Parameters
    ----------
    *args : list(Plot A, [Plot B], ...)
        Plot data (x, y) to build our plots from.
    x_min : int
        Minimum limit on the x-axis to plot.
    x_max : int
        Maximum limit on the x-axis to plot.

    Returns
    -------
    fig : matplotlib.pyplot.Figure
        Figure object that was created and displayed.

    """
    plt.close()
    fig, ax = plt.subplots()

    integrator_result, = ax.plot(args[0][0], args[0][1], '-')
    mhd_result, = ax.plot(args[1][0], args[1][1], '-')
    ax.legend(handles=[integrator_result, mhd_result],
              labels=['Biot Savart Integrator Result', 'MHD Result'])
    ax.set_title('MHD vs. Integrator Results')
    ax.set_ylabel(r'$B_z \ (nT)$')
    ax.set_xlabel('time (m)')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1.0))
    if x_min is None or x_max is None:
        x_min, x_max = ax.get_xlim()
    else:
        ax.set_xlim(x_min, x_max)

    ax.xaxis.set_minor_locator(ticker.MaxNLocator(5 * (x_max - x_min)))
    plt.show()
    return fig


def export_figure(figure, filepath):
    """
    Export a figure to a provided filepath, creates path if it does not exist.

    Parameters
    ----------
    figure : matplotlib.pyplot.Figure
        The figure to export as an svg file.
    filepath : str
        Filepath, including file name, where the svg should be saved.

    Returns
    -------
    None.

    """
    fp = filepath.rsplit('/', 1)[0]
    if not isdir(fp):
        makedirs(fp)
    figure.savefig(filepath)
