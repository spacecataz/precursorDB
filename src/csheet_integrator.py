'''
A module for calculating the proposed ground perturbation due
to a interplanetary current sheet before it comes in contact with the 
Earth's upstream bow shock.
'''

import numpy as np

### Some useful constants:
mu0 = 4*np.pi*1E-7
Re  = 6371000 # Earth radius in meters.


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

def gen_kernal(R, ky, kz):
    '''
    Create functions that represent the kernal for the integral, both for
    by and bz.

    ###i'm tooo lazy to change this now.
    The function that is the integral kernal for the biot-savart function.
    "R" is the distance of the center of the sheet from Earth (r-x) and
    y, z are the coordinates along the sheet where we are currently 
    integrating.
    Kx, Ky are the strength of the current sheet.
    Returns: Bz portion of integral kernal.
    UNITS: Use meters and amp/meters.  SI, fool.
    '''

    by = lambda y,z: 0
    bz = lambda y,z: (kx*y-ky*R)/np.sqrt( np.sqrt(y**2+z**2) + R**2 )
    
    return by, bz
    
def biot_savart(R, ky, kz, width=128, dX=.1):
    '''
    Using the midpoint integrator, calculate the surface magnetic field
    perturbation from a uniform interplanetary current sheet.

    Parameters:
    ==========
    R : float
        Distance from Earth in Earth radii
    ky : float 
        Current sheet strength in the GSM Y-direction (amps/m)
    kz : float 
        Current sheet strength in the GSM Y-direction (amps/m)
    

    Other parameters:
    =================
    width : float
        Width of current sheet in both Y and Z directions in Re.
        Defaults to 128 earth radii.
    dx    : float
        Size of spatial step for integration in Earth radii.
        Defaults to .1Re.

    Returns:
    ===========
    by, bz : float, float
        Perturbation as measured by ground at center of Earth in the
        Y, Z directions (GSM).

    '''

    # Convert units!
    R     *=Re  #earth radii to meters.
    #width *=Re  #earth radii to meters.
    #dX    *=Re  #earth radii to meters.

    # Get number of steps required to finish integral:
    nx = int(width/dX)

    # Create integral kernals:
    kern_y, kern_z = gen_kernal(R, ky, kz)
    
    # Integrate!
    by = 0 # Hey fix this in the future.
    bz = midpoint(_biot_kernal_z, width/2, width/2, width/2, width/2, nx, nx)

    return(bz)
    
def calc_K(b1, b2):
    '''
    For *b1* (downstream magnetic field, or field closer to the Earth)
    and *b2* (upstream magnetic field, or further from the Earth), calculate
    the current sheet required to sustain the change between the fields.
    Return current density in amperes/meter.

    Magnetic field should be given in nanotesla!
    '''

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

    # To get time series, loop over an array of R-values:
    x_all = np.arange(150, 15, -1)
    b_all = np.zeros(x.size)

    for i, x in enumerate(x_all):
        b_all[i] = biot_savart(x, Ky, Kz)
