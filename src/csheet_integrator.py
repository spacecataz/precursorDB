"""
Module that calculates the ground perturbation from a current sheet.

Calculates the proposed ground perturbation due to an interplanetary current
sheet before it comes in contact with the Earth's upstream bow shock.
"""

import numpy as np
from os.path import exists, split
from os import makedirs
from enum import IntEnum
import json

# Some useful constants:
mu0 = 4 * np.pi * 1E-7
Re = 6371000  # Earth radius in meters.


def midpointYZ(f, y_start, y_end, y_n, z_start, z_end, z_n):
    """
    Approximate the integral for 'f(y, z) dy dz' using the Midpoint Rule.

    Parameters
    ----------
    f : lambda (m_y, m_z)
        The function, f(m_i), in the Midpoint Summation for M_n.
    y_start : float
        The starting y position of the current sheet to integrate over.
    y_end : float
        The ending y position of the current sheet to integrate over.
    y_n : int
        The n value for the y axis; the number of intervals the range
        of y values should be divided into.
    z_start : float
        The starting z position of the current sheet to integrate over.
    z_end : float
        The ending z position of the current sheet to integrate over.
    z_n : int
        The n value for the z axis; the number of intervals the range
        of z values should be divided into.

    Returns
    -------
    result : float
        The approximated result of the integral for 'f(a) da'.

    """
    # Function for the DeltaX components of the midpoint rule
    def delta(a, b, n):
        return (b - a) / n

    # Get the DeltaY and DeltaZ values
    del_y = delta(y_start, y_end, y_n)
    del_z = delta(z_start, z_end, z_n)

    result = 0
    # Iterate over the range of all intervals in the y-axis
    for i in range(y_n):
        # Calculate the position of the y-midpoint for this interval
        y_position = y_start + (del_y / 2) + (del_y * i)
        # Iterate over intervals in the z-axis for each y-axis interval
        for j in range(z_n):
            # Calculate the position of the z-midpoint for this interval
            z_position = z_start + (del_z / 2) + (del_z * j)
            # Add the calculated value for the summation at this y-z interval
            result += (del_y * del_z) * f(y_position, z_position)
    return result


def test_midpointYZ(tol=1E-5):
    """
    Test the midpointYZ() function using ideal.

    Parameters
    ----------
    tol : float, optional
        Tolerance of error in the result. The default is 1E-5.

    Returns
    -------
    None.

    """
    expected = 9.0  # This should be what we get
    success = True

    def f(y, z):
        return 2 * y + z

    result = midpointYZ(f, 0, 2, 5, 2, 3, 5)
    diff = np.abs(result - expected)

    if diff > tol:
        success = False

    print('Test {}:\n  Result   | {}\n  Expected | {}\n  Success  | {}'
          .format('midpointYZ', result, expected, success))


def gen_kernel(R, ky, kz):
    """
    Create kernel functions for the biot-savart integrals.

    Parameters
    ----------
    R : float
        Distance in meters from the Earth to the center of current sheet (r-x).
    ky : float
        Current sheet strength in the GSM Y-direction (amps/m).
    kz : float
        Current sheet strength in the GSM Z-direction (amps/m).

    Returns
    -------
    y_kernel : lambda
        Integral kernel function for the GSM Y-direction.
    z_kernel : lambda
        Integral kernel function for the GSM Z-direction.

    Notes
    -----
    y : float
        GSM Y-coortinate along the current sheet where we are integrating.
    z : float
        GSM Z-coordinate along the current sheet where we are integrating.

    """
    def y_kernel(y, z):
        r_total = np.sqrt(R**2 + y**2 + z**2)
        rhat_x = -R/r_total
        return kz * rhat_x / r_total**2

    def z_kernel(y, z):
        r_total = np.sqrt(R**2 + y**2 + z**2)
        rhat_x = -R/r_total
        return -ky * rhat_x / r_total**2

    return y_kernel, z_kernel


def biot_savart(R, ky, kz, width=128, dX=0.1):
    """
    Calculate surface magnetic field perturbation from a uniform current sheet.

    Parameters
    ----------
    R : float
        Distance from the Earth to the center of current sheet (r-x, meters).
    ky : float
        Current sheet strength in the GSM Y-direction (amps/m).
    kz : float
        Current sheet strength in the GSM Z-direction (amps/m).
    width : float, optional
        Width of current sheet in Y and Z directions (Re). The default is 128.
    dX : float, optional
        Size of spatial step for integration (Re). The default is 0.1.

    Returns
    -------
    by : float
        Perturbation measured by ground at center of Earth in GSM Y-direction.
    bz : float
        Perturbation measured by ground at center of Earth in GSM Z-direction.

    """
    halfw = width * Re / 2  # Units: m

    # Get number of steps required to finish integral
    nx = int(width / dX)

    # Create integral kernels
    kern_y, kern_z = gen_kernel(R, ky, kz)

    # Integrate to solve for by, bz.  Units: Amps
    by = 0
    bz = midpointYZ(kern_z, -halfw, halfw, nx, -halfw, halfw, nx)

    # Convert to nanotesla from Amps.  4piE-7/4pi = 1E-7 => 1E-7 * 1E9 = 1E2
    by *= 1E2
    bz *= 1E2

    return(by, bz)  # Units: nT


def test_biot_savart(tol=1E-5):
    """
    Test the biot_savart() function using a known solution.

    Parameters
    ----------
    tol : float, optional
        Tolerance of error in the result. The default is 1E-5.

    Returns
    -------
    None.

    """
    expected = (0, 0)
    success = True

    result = biot_savart(0, 0, 0)
    diff = tuple(map(lambda a, b: np.abs(a - b), result, expected))

    if diff[0] > tol or diff[1] > tol:
        success = False

    print('Test {}:\n  Result   | {}\n  Expected | {}\n  Success  | {}'
          .format('biot_savart', result, expected, success))


def calc_K(IMFd, IMFu):
    """
    Calculate K of the current sheet from magnetic fields on either side.

    Parameters
    ----------
    IMFd : float
        Downstream magnetic field in nanotesla (closer to the Earth).
    IMFu : float
        Upstream magnetic field in nanotesla (further from the Earth).

    Returns
    -------
    float
        Current density K in amperes/meter.

    Notes
    -----
    The calculation here takes into account the direction such that dL around
        our amperian loop is in the positive Z direction on the b1 side.

    """
    return 1E-9 * (IMFd*(1) + IMFu*(-1)) / mu0  # Units: A/m


class eGSM(IntEnum):
    """Enum for indexing the x, y, and z components of GSM vectors."""

    x = 0
    y = 1
    z = 2


def gmp_timeseries(IMFd, IMFu, Vsw, dT=60, r0=100, w_csheet=128, dI=1.0):
    """
    Solve for time series of ground magnetic perturbation due to current sheet.

    Parameters
    ----------
    IMFd : ndarray<float> (vector)
        Downstream IMF vector in GSM coordinates (Earth side of current sheet).
    IMFu : ndarray<float> (vector)
        Upstream IMF vector in GSM coordinates (Sun side of current sheet).
    Vsw : ndarray<float>
        Solar wind velocity vector in GSM coordinates (km/s).
    dT : int, optional
        Time between integrations (s). The default is 60.
    r0 : int, optional
        Initial X position of the current sheet (RE). The default is 100.
    w_csheet : float, optional
        Width of current sheet in Y and Z directions (Re). The default is 128.
    dI : float, optional
        Size of spatial step for integration (Re). The default is 1.0.

    Returns
    -------
    numpy.array
        json object
            Input values used to generate this timeseries
        series of tuples
            t_elapsed, By, and Bz.  Units: s, nT, nT

    """
    timeseries = [{'IMFd': IMFd, 'IMFu': IMFu,
                   'Vsw': Vsw, 'dT': dT, 'r0': r0,
                   'w_csheet': w_csheet, 'dI': dI}]

    listtypes = [list, np.ndarray]

    if (type(IMFd) not in listtypes
            or type(IMFu) not in listtypes
            or type(Vsw) not in listtypes):
        # Using old input formatting
        errstr = ('Input format is deprecated, please use iterables in GSM ' +
                  'coordinates as input for \'IMFd\', \'IMFu\', and \'Vsw\' ' +
                  '(e.g. [x, y, z])')
        print(errstr)
        return np.array(timeseries)

    floattypes = [float, np.float32, np.float64]
    if type(IMFd) is not np.ndarray or type(IMFd[0]) not in floattypes:
        IMFd = np.array(list(IMFd), float)
    if type(IMFu) is not np.ndarray or type(IMFu[0]) not in floattypes:
        IMFu = np.array(list(IMFu), float)
    if type(Vsw) is not np.ndarray or type(Vsw[0]) not in floattypes:
        Vsw = np.array(list(Vsw), float)

    # Get our current sheet strength using values from simulation:
    Ky = calc_K(IMFd[eGSM.z], IMFu[eGSM.z])  # (-5, 127)
    Kz = calc_K(IMFd[eGSM.y], IMFu[eGSM.y])
    print(f"Ky = {Ky:0.4f} | Kz = {Kz:0.4f}")

    # Convert distance of current sheet from Earth to RE:
    R = r0 * Re

    dX = Vsw[eGSM.x] * 1000.0 * dT

    x_position = R
    t_elapsed = 0

    # Adjust x pos by -dX so we stop after the first integration below 10RE
    while (x_position > 5 * Re) and (x_position > (10 * Re) + dX):
        line = f"X: {x_position/Re:12.4f}RE | T: {t_elapsed:5.1f}s | "
        by, bz = biot_savart(x_position, Ky, Kz, w_csheet, dI)
        print(line + f"By: {by:0.2e}nT | Bz: {bz:0.2e}nT")
        timeseries.append((t_elapsed, by, bz))
        t_elapsed += dT
        x_position += dX

    return np.array(timeseries)


def export_timeseries(ts, export_filepath="ts_export",
                      replace_existing=False, create_missing_paths=True):
    """
    Export a timeseries generated by gmp_timeseries() to a text file.

    Parameters
    ----------
    ts : numpy.array
        Timeseries of t_elapsed, By, and Bz.  Units: s, nT, nT.
    export_filepath : str, optional
        Path to file for export. The default is "ts_export".
    replace_existing : bool, optional
        Should an already existing file be replaced. The default is False.

    Returns
    -------
    None.

    """
    if type(export_filepath) is not str:
        export_filepath = "ts.txt"
    if not export_filepath.endswith(".txt"):
        export_filepath += ".txt"
    path = split(export_filepath)
    if path[0] != '' and not exists(path[0]):
        if create_missing_paths:
            makedirs(path[0])
        else:
            print(f'Path not found ({path[0]}), file was not exported.')
            return

    if exists(export_filepath):
        if replace_existing:
            open(export_filepath, 'w').close()
        else:
            epath = export_filepath[:-4]
            i = 2
            while exists(epath + '_' + str(i) + ".txt"):
                i += 1

            export_filepath = epath + '_' + str(i) + ".txt"

    with open(export_filepath, 'w') as fp:
        fp.write(json.dumps(ts[0]) + "\n")
        for row in ts[1:]:
            line = ""
            for value in row:
                line += str(value) + ' '
            fp.write(line.strip() + "\n")


def import_timeseries(import_filepath):
    """
    Import a timeseries from a text file generated by export_timeseries().

    Parameters
    ----------
    import_filepath : str
        Path to the file that the timeseries should be imported from.

    Returns
    -------
    numpy.array
        Timeseries of t_elapsed, By, and Bz.  Units: s, nT, nT.
        If import_filepath is not a valid file, returns None.

    """
    if type(import_filepath) is not str:
        return None
    if not import_filepath.endswith(".txt"):
        import_filepath += ".txt"
    if exists(import_filepath):
        timeseries = []
        with open(import_filepath, 'r') as fp:
            for line in fp:
                if len(timeseries) == 0:
                    timeseries.append(json.loads(line))
                    continue
                attributes = line.split()
                attr_map = map(float, attributes)
                attr_list = list(attr_map)
                timeseries.append(attr_list)
        return np.array(timeseries)
    else:
        return None


if __name__ == '__main__':
    # This is the default action if you run this code
    ts = gmp_timeseries(
        [0, 0, -5], [0, 0, 127], [-2700, 0, 0], dI=1.0)

    # export_timeseries(ts, 'ts_json_test.txt')
    # json_dict = import_timeseries('ts_json_test.txt')

    # ts = gmp_timeseries(-5, 127, -2700, dI=1.0)
    # export_timeseries(ts, 'ts_json_test2.txt')

    # for dI in range(1, 100, 1):  # np.arange(0.01, 0.11, 0.01):
    #     ts = gmp_timeseries(
    #         [0, 0, -5], [0, 0, 127], [-2700, 0, 0], dI=round(dI * 0.1, 1))
    #     export_timeseries(ts, f'ts_out_{round(dI * 0.1, 1)}.txt')
