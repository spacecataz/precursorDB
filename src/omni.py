#!/usr/bin/env python
'''
A module for obtaining (eventually) and parsing data from
http://omniweb.gsfc.nasa.gov/
'''

import re
import datetime as dt
import numpy as np
from spacepy.datamodel import dmarray

def read_ascii(filename):
    '''
    Load data into dictionary.
    '''

    if filename[-4:] == '.lst':
        datafile   = filename
        formatfile = filename[:-4]+'.fmt'
    elif filename[-4:] == '.fmt':
        formatfile = filename
        datafile   = filename[:-4]+'.lst'
    else:
        formatfile = filename+'.fmt'
        datafile   = filename+'.lst'

    try:
        fmt = open(formatfile, 'r')
    except:
        fmt = False

    info = {}
    var  = []
    flag = []
       
    if fmt:
        raw = fmt.readlines()
        fmt.close()
        # Determine time resolution: hour or minute:
        tres = 'Hour'
        for line in raw:
            if 'Minute' in line: tres='Minute'
       
        # Skip header.
        while True:
            raw.pop(0)
            if tres in raw[0]: break
        last = raw.pop(0)

        # Parse rest of header:
        for l in raw:
            # This regular expression skips the initial digit & space,
            # Lazily grabs the variable name (? turns off greed in this context)
            #
            x = re.search('\d+\s+(.+?)\s+([FI]\d+\.?\d*)', l)
            #x=re.search('\d+\s+(.+?),\s*(\S+)', l) # Old, breaks w/o units.
            if x:
                grps = x.groups()
                # If units available, split and keep:
                var_units = grps[0].split(',')
                if len(var_units)==1: var_units.append('None')
                info[var_units[0]] = ','.join(var_units[1:])
                var.append(var_units[0])
                fmt_code = grps[-1]
                if 'F' in fmt_code:
                    i1, i2 = int(fmt_code[1]), -1*int(fmt_code[-1])
                    flag.append(10**(i1+i2-2) - 10**(i2))
                elif 'I' in fmt_code:
                    i1 = int(fmt_code[-1])-1
                    flag.append(10**i1 -1)
            else:
                raise ValueError(f'Cannot parse header line: {l}')
       
    # Read in data.
    raw = open(datafile, 'r').readlines()
    nLines = len(raw)

    # Create container.
    data = {}
    data['time'] = np.zeros(nLines, dtype=object)
    for k in info:
        data[k] = np.zeros(nLines)
        #data[k] = dmarray(np.zeros(nLines), attrs={'units':info[k]})
    
    # Now save data.
    t_index = 3 + (tres == 'Minute')*1
    for i, l in enumerate(raw):
        parts = l.split()
        doy = dt.timedelta(days=int(parts[1])-1)
        minute = int(float(parts[3]))*(tres == 'Minute')
        data['time'][i]=dt.datetime(int(parts[0]), 1, 1, int(parts[2]),
                                    minute, 0) + doy
        for j, k in enumerate(var):
            data[k][i] = parts[j+t_index]

    # Mask out bad data.
    for i, k in enumerate(var):
        data[k] = np.ma.masked_greater_equal(data[k], flag[i])

           
    return data

def omni_to_swmf(infile, outfile=None):
    '''
    Given an input omni file, *infile*, read its contents and convert to an
    SWMF input file.  The omni input file **must** have the following
    variables: BX, BY, BZ (all GSM); Proton Density; Speed; Temperature.

    If the kwarg *outfile* is set, the resulting conversion will be written
    to the file specified by the kwarg.
   
    Both the omni data and the ImfInput object are returned to the caller.

    This function will attempt to linearly interpolate over bad data values.
    If the first or last line of the data contains bad data flags, this will
    fail.

    GSE coordinates V_Y and V_Z will be rotated to GSM coordinates.

    Finally, always inspect your results.
    '''

    from spacepy.pybats import ImfInput
    from spacepy.time import Ticktock
    from spacepy.coordinates import Coords
    from validate import pairtimeseries_linear as pair
   
    # Variable name mapping:
    omVar = ['BX', 'BY', 'BZ', 'Vx Velocity', 'Vy Velocity', 'Vz Velocity', 'Proton Density', 'Temperature']
    swVar = ['bx', 'by', 'bz', 'ux',          'uy',          'uz',          'rho',            'temp'       ]
    #omVar = ['BX', 'BY', 'BZ', 'Speed', 'Proton Density', 'Temperature']

    # Load observations:
    omdat = read_ascii(infile)
    nPts = omdat['time'].size
   
    # Create empty ImfInput object:
    swmf = ImfInput(npoints=nPts, load=False, filename=outfile)
   
    # Convert data and load into ImfInput object:
    swmf['time'] = omdat['time']
    npts = swmf['time'].size
    for vo, vs in zip(omVar, swVar):
        if vo in omdat:
            swmf[vs] = pair(omdat['time'], omdat[vo], omdat['time'])
        else:
            print('WARNING: Did not find {} in Omni file.'.format(vo))
            swmf[vs] = np.zeros(npts)

    # Do rotation of Vy, Vz GSE->GSM:
    rot = Coords(np.array([swmf['ux'], swmf['uy'], swmf['uz']]).transpose(),
                 'GSE', 'car', ['Re','Re','Re'],
                 Ticktock(swmf['time'])).convert('GSM', 'car')

    # Copy rotated values into original structure:
    swmf['ux'] = rot.data[:,0]
    swmf['uy'] = rot.data[:,1]
    swmf['uz'] = rot.data[:,2]
           
    # Flip sign of velocity:
    if swmf['ux'].min() >0: swmf['ux'] *= -1

    if outfile: swmf.write()
       
    return omdat, swmf

def qindent_to_swmf(infiles, outfile):
    '''
    Given either a single input file name or a list of multiple file names
    corresponding to JSON-headed ASCII Qin-Denton OMNI data (obtainable from
    http://www.rbsp-ect.lanl.gov/data_pub/QinDenton), this function will
    produce an SWMF IMF input file.

    If the kwarg *outfile* is set, the resulting conversion will be written
    to the file specified by the kwarg.
   
    Both the omni data and the ImfInput object are returned to the caller.

    This function will attempt to linearly interpolate over bad data values.
    If the first or last line of the data contains bad data flags, this will
    fail.

    There are many limitations to this approach.  First, V_Y and V_Z are
    set to zero as this information is not given in the Qin-Denton files.
    The same is true for IMF Bx.  Finally, and most importantly, solar
    wind temperature is not present, making this whole thing really bad.

    A limitation of this approach is that solar V_Y, V_Z are neglected.  
    Additionally, there is no B_X information, so these values are set to
    zero as well.  Use with care!

    Finally, always inspect your results.
    '''

    from spacepy.omni import readJSONheadedASCII as readit
    from spacepy.pybats import ImfInput
    from validate import pairtimeseries_linear as pair

    raise NotImplemented('This function is incomplete.')
   
    return False
   
    # Variable names:
    omVar = ['ByIMF', 'BzIMF', 'Vsw', 'Den_P', 'Temperature']
    swVar = ['by',    'bz',    'ux',  'rho',   'temp'       ]

    # Read omni files:
    omdat = readit(infiles)

    # Create empty ImfInput object:
    nPts = omdat['time'].size
    swmf = ImfInput(npoints=nPts, load=False, filename=outfile)
   
    return omdat, swmf