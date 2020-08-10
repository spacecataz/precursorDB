'''
A module for calculating the proposed ground perturbation due
to a interplanetary current sheet before it comes in contact with the 
Earth's upstream bow shock.
'''

import numpy as np

### Some useful constants:
mu0 = 4*np.pi*1E-7
Re  = 6371000 # Earth radius in meters.

def midpointYZ(f, y_start, y_end, y_n, z_start, z_end, z_n):
    """
    Calculates an approximation of the integral for 'f(a) da' using the
        Midpoint Rule. Here our values of da are on the y-z plane.

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
        DESCRIPTION.

    """
    # Function for the DeltaX components of the midpoint rule
    delta = lambda a, b, n: (b - a) / float(n)
    
    # Get the DeltaY and DeltaZ values
    del_y = delta(y_start, y_end, y_n)
    del_z = delta(z_start, z_end, z_n)
    
    result = 0
    # Iterate over the range of all intervals in the y-axis
    for dy in range(y_n):
        # Calculate the position of the y-midpoint for this interval
        y_position = y_start + (del_y/float(2)) + (del_y * dy)
        # Iterate over the range of all intervals in the z-axis for each y-axis interval
        for dz in range(z_n):
            # Calculate the position of the z-midpoint for this interval
            z_position = z_start + (del_z/float(2)) + (del_z * dz)
            # Add the calculated value for the summation at this y-z interval
            result += (del_y * del_z) * f(y_position, z_position)
    return result


def midpoint(f, a, b, c, d, nx, ny):
    '''
    Description of function and all inputs. <3
    '''
    
    hx = (b - a)/float(nx)
    hy = (d - c)/float(ny)
    I = 0
    for i in range(nx):
        for j in range(ny):
            xi = a + hx/2 + i*hx
            yj = c + hy/2 + j*hy
            I += hx*hy*f(xi, yj)
    return I

def test_midpoint(tol = 1E-5):
    '''
    Test our midpoint problem using ideal
    '''

    f = lambda x, y: 2*x + y
    result = midpoint(f, 0, 2, 2, 3, 5, 5)

    expected = 9.0 # This should be what we get!

    # If result is different than expected answer more than
    # a set tolerance, throw a fit.
    if np.abs(result-expected) > tol:
        print('Result = {}, Expected = {}'.format(result, expected))
        raise ValueError('Did not return correct result!!!')

def gen_kernel(R, ky, kz):
    '''
    Create functions that represent the kernel for the integral, both for
    by and bz.

    ###i'm tooo lazy to change this now.
    The function that is the integral kernel for the biot-savart function.
    "R" is the distance of the center of the sheet from Earth (r-x) and
    y, z are the coordinates along the sheet where we are currently 
    integrating.
    Kx, Ky are the strength of the current sheet.
    Returns: Bz portion of integral kernel.
    UNITS: Use meters and amp/meters.  SI, fool.
    '''
    
# These need to be checked over.
    by = lambda y,z: 0 
    bz = lambda y,z: 0 #(kx*y-ky*R)/np.sqrt( np.sqrt(y**2+z**2) + R**2 )
    
    return by, bz
    
def biot_savart(R, ky, kz, width=128, dX=0.1):
    '''
    Using the midpoint integrator, calculate the surface magnetic field
    perturbation from a uniform interplanetary current sheet.

    Parameters:
    ==========
    R : float
        Distance from Earth in meters
    ky : float 
        Current sheet strength in the GSM Y-direction (amps/m)
    kz : float 
        Current sheet strength in the GSM Z-direction (amps/m)
    

    Other parameters:
    =================
    width : float
        Width of current sheet in both Y and Z directions in Re.
        Defaults to 128 earth radii.
    dX    : float
        Size of spatial step for integration in Earth radii.
        Defaults to 0.1Re.

    Returns:
    ===========
    by, bz : float, float
        Perturbation as measured by ground at center of Earth in the
        Y, Z directions (GSM).

    '''

    # Get number of steps required to finish integral:
    nx = int(width/dX)

    # Create integral kernels:
    kern_y, kern_z = gen_kernel(R, ky, kz)
    
    # Integrate!
    # by = 0 # Hey fix this in the future.
    bz = midpoint(kern_z, width/2, width/2, width/2, width/2, nx, nx)
    
    return(bz)
    
def calc_K(b1, b2):
    '''
    For *b1* (downstream magnetic field, or field closer to the Earth)
    and *b2* (upstream magnetic field, or further from the Earth), calculate
    the current sheet required to sustain the change between the fields.
    Return current density in amperes/meter.

    Magnetic field should be given in nanotesla!
    '''
    
# Does this match our calculations?
    return 1E-9*(b1-b2)/mu0
    
if __name__ == '__main__':
    # This is the default action if you run this code!
    print('Testing against Extreme SSI simulation!')

    # Get our current sheet strength using values from simulation:
    Ky = calc_K(-5, 127)
    Kz = 0
    
    # Set distance from Earth:
    R = 20 * Re # 20 RE from Earth! 
    
    # Integrate!
    bz = biot_savart(R, Ky, Kz)
    
# I'm not sure what this does.
    # To get time series, loop over an array of R-values:
    x_all = np.arange(150, 15, -1)
    b_all = np.zeros(x_all.size)

    for i, x in enumerate(x_all):
        b_all[i] = biot_savart(x, Ky, Kz)
