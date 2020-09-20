"""
Module that calculates the ground perturbation from a current sheet.

Calculates the proposed ground perturbation due to an interplanetary current
sheet before it comes in contact with the Earth's upstream bow shock.
"""

import numpy as np

# Some useful constants:
mu0 = 4*np.pi*1E-7
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
    def delta(a, b, n): return (b - a) / float(n)

    # Get the DeltaY and DeltaZ values
    del_y = delta(y_start, y_end, y_n)
    del_z = delta(z_start, z_end, z_n)

    result = 0
    # Iterate over the range of all intervals in the y-axis
    for dy in range(y_n):
        # Calculate the position of the y-midpoint for this interval
        y_position = y_start + (del_y/float(2)) + (del_y * dy)
        # Iterate over intervals in the z-axis for each y-axis interval
        for dz in range(z_n):
            # Calculate the position of the z-midpoint for this interval
            z_position = z_start + (del_z/float(2)) + (del_z * dz)
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

    Raises
    ------
    ValueError
        Raise when result is outside of tolerance.

    Returns
    -------
    None.

    """
    def f(y, z): return 2*y + z
    result = midpointYZ(f, 0, 2, 5, 2, 3, 5)
    expected = 9.0  # This should be what we get
    success = True

    if np.abs(result-expected) > tol:
        success = False

    print('Test midpointYZ:\n  Result   | {}\n  Expected | {}\n  Success  | {}'
          .format(result, expected, success))


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
    '''These need to be checked over.'''
    def y_kernel(y, z): return 0
    # Old Equation for z: (kx*y-ky*R)/np.sqrt( np.sqrt(y**2+z**2) + R**2 )
    def z_kernel(y, z): return 0  # Temporarily zeroed.

    return y_kernel, z_kernel


def biot_savart(R, ky, kz, width=128, dX=0.1):
    """
    Calculate surface magnetic field perturbation from a uniform current sheet.

    Parameters
    ----------
    R : float
        Distance from the Earth to the center of current sheet (r-x).
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
    # Get number of steps required to finish integral:
    nx = int(width/dX)

    # Create integral kernels:
    kern_y, kern_z = gen_kernel(R, ky, kz)

    # Integrate to solve for by, bz.
    by = 0  # Hey fix this in the future.
    bz = midpointYZ(kern_z, width/2, width/2, width/2, width/2, nx, nx)

    return(by, bz)


def calc_K(b1, b2):
    """
    Calculate K of the current sheet from magnetic fields on either side.

    Parameters
    ----------
    b1 : float
        Downstream magnetic field in nanotesla (closer to the Earth).
    b2 : float
        Upstream magnetic field in nanotesla (further from the Earth).

    Returns
    -------
    float
        Current density K in amperes/meter.

    """
    # Does this match our calculations?
    return 1E-9*(b1-b2)/mu0


def main_old():
    """
    Old contents of main.

    Returns
    -------
    None.

    """
    print('Testing against Extreme SSI simulation!')

    # Get our current sheet strength using values from simulation:
    Ky = calc_K(-5, 127)
    Kz = 0

    # Set distance from Earth:
    R = 20 * Re  # 20 RE from Earth

    # Integrate!
    by, bz = biot_savart(R, Ky, Kz)
    print(bz)

    ''' I'm not sure what this does.'''
    # To get time series, loop over an array of R-values:
    x_all = np.arange(150, 15, -1)
    b_all = np.zeros(x_all.size)

    for i, x in enumerate(x_all):
        trash, b_all[i] = biot_savart(x, Ky, Kz)


if __name__ == '__main__':
    # This is the default action if you run this code
    test_midpointYZ()
    # main_old()
