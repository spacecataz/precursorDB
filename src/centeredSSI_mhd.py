import matplotlib.pyplot as plt
from spacepy.pybats import bats
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import numpy as np
from spacepy.plot import style
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from matplotlib.lines import Line2D

def mhd(filename):
    LT = int(filename[-11:-9])
    mag = bats.MagFile(filename)
    t = mag['time']
    mhd = np.zeros(shape = (3, 15, 8101))

	#convert MHD vectors to SM coordinates
    mhd[0] = np.array([-mag['d10']['dBnMhd'] * np.cos((np.pi/2)-(10 * np.pi / 180)) * np.cos(LT * np.pi /12) - mag['d10']['dBdMhd'] * np.sin((np.pi/2)-(10 * np.pi / 180)) * np.cos(LT * np.pi/12) - mag['d10']['dBeMhd'] * np.sin(LT*np.pi/12),
                       -mag['d15']['dBnMhd'] * np.cos((np.pi/2)-(15 * np.pi / 180)) * np.cos(LT * np.pi /12) - mag['d15']['dBdMhd'] * np.sin((np.pi/2)-(15 * np.pi / 180)) * np.cos(LT * np.pi/12) - mag['d15']['dBeMhd'] * np.sin(LT*np.pi/12),
                       -mag['d20']['dBnMhd'] * np.cos((np.pi/2)-(20 * np.pi / 180)) * np.cos(LT * np.pi /12) - mag['d20']['dBdMhd'] * np.sin((np.pi/2)-(20 * np.pi / 180)) * np.cos(LT * np.pi/12) - mag['d20']['dBeMhd'] * np.sin(LT*np.pi/12),
                       -mag['d25']['dBnMhd'] * np.cos((np.pi/2)-(25 * np.pi / 180)) * np.cos(LT * np.pi /12) - mag['d25']['dBdMhd'] * np.sin((np.pi/2)-(25 * np.pi / 180)) * np.cos(LT * np.pi/12) - mag['d25']['dBeMhd'] * np.sin(LT*np.pi/12),
                       -mag['d30']['dBnMhd'] * np.cos((np.pi/2)-(30 * np.pi / 180)) * np.cos(LT * np.pi /12) - mag['d30']['dBdMhd'] * np.sin((np.pi/2)-(30 * np.pi / 180)) * np.cos(LT * np.pi/12) - mag['d30']['dBeMhd'] * np.sin(LT*np.pi/12),
                       -mag['d35']['dBnMhd'] * np.cos((np.pi/2)-(35 * np.pi / 180)) * np.cos(LT * np.pi /12) - mag['d35']['dBdMhd'] * np.sin((np.pi/2)-(35 * np.pi / 180)) * np.cos(LT * np.pi/12) - mag['d35']['dBeMhd'] * np.sin(LT*np.pi/12),
                       -mag['d40']['dBnMhd'] * np.cos((np.pi/2)-(40 * np.pi / 180)) * np.cos(LT * np.pi /12) - mag['d40']['dBdMhd'] * np.sin((np.pi/2)-(40 * np.pi / 180)) * np.cos(LT * np.pi/12) - mag['d40']['dBeMhd'] * np.sin(LT*np.pi/12),
                       -mag['d45']['dBnMhd'] * np.cos((np.pi/2)-(45 * np.pi / 180)) * np.cos(LT * np.pi /12) - mag['d45']['dBdMhd'] * np.sin((np.pi/2)-(45 * np.pi / 180)) * np.cos(LT * np.pi/12) - mag['d45']['dBeMhd'] * np.sin(LT*np.pi/12),
                       -mag['d50']['dBnMhd'] * np.cos((np.pi/2)-(50 * np.pi / 180)) * np.cos(LT * np.pi /12) - mag['d50']['dBdMhd'] * np.sin((np.pi/2)-(50 * np.pi / 180)) * np.cos(LT * np.pi/12) - mag['d50']['dBeMhd'] * np.sin(LT*np.pi/12),
                       -mag['d55']['dBnMhd'] * np.cos((np.pi/2)-(55 * np.pi / 180)) * np.cos(LT * np.pi /12) - mag['d55']['dBdMhd'] * np.sin((np.pi/2)-(55 * np.pi / 180)) * np.cos(LT * np.pi/12) - mag['d55']['dBeMhd'] * np.sin(LT*np.pi/12),
                       -mag['d60']['dBnMhd'] * np.cos((np.pi/2)-(60 * np.pi / 180)) * np.cos(LT * np.pi /12) - mag['d60']['dBdMhd'] * np.sin((np.pi/2)-(60 * np.pi / 180)) * np.cos(LT * np.pi/12) - mag['d60']['dBeMhd'] * np.sin(LT*np.pi/12),
                       -mag['d65']['dBnMhd'] * np.cos((np.pi/2)-(65 * np.pi / 180)) * np.cos(LT * np.pi /12) - mag['d65']['dBdMhd'] * np.sin((np.pi/2)-(65 * np.pi / 180)) * np.cos(LT * np.pi/12) - mag['d65']['dBeMhd'] * np.sin(LT*np.pi/12),
                       -mag['d70']['dBnMhd'] * np.cos((np.pi/2)-(70 * np.pi / 180)) * np.cos(LT * np.pi /12) - mag['d70']['dBdMhd'] * np.sin((np.pi/2)-(70 * np.pi / 180)) * np.cos(LT * np.pi/12) - mag['d70']['dBeMhd'] * np.sin(LT*np.pi/12),
                       -mag['d75']['dBnMhd'] * np.cos((np.pi/2)-(75 * np.pi / 180)) * np.cos(LT * np.pi /12) - mag['d75']['dBdMhd'] * np.sin((np.pi/2)-(75 * np.pi / 180)) * np.cos(LT * np.pi/12) - mag['d75']['dBeMhd'] * np.sin(LT*np.pi/12),
                       -mag['d80']['dBnMhd'] * np.cos((np.pi/2)-(80 * np.pi / 180)) * np.cos(LT * np.pi /12) - mag['d80']['dBdMhd'] * np.sin((np.pi/2)-(80 * np.pi / 180)) * np.cos(LT * np.pi/12) - mag['d80']['dBeMhd'] * np.sin(LT*np.pi/12)])

    mhd[1] = np.array([-mag['d10']['dBnMhd'] * np.cos((np.pi/2)-(10 * np.pi / 180)) * np.sin(LT * np.pi / 12) - mag['d10']['dBdMhd'] * np.sin((np.pi/2)-(10 * np.pi / 180)) * np.sin(LT * np.pi/12) + mag['d10']['dBeMhd'] * np.cos(LT*np.pi/12),
                       -mag['d15']['dBnMhd'] * np.cos((np.pi/2)-(15 * np.pi / 180)) * np.sin(LT * np.pi / 12) - mag['d15']['dBdMhd'] * np.sin((np.pi/2)-(15 * np.pi / 180)) * np.sin(LT * np.pi/12) + mag['d15']['dBeMhd'] * np.cos(LT*np.pi/12),
                       -mag['d20']['dBnMhd'] * np.cos((np.pi/2)-(20 * np.pi / 180)) * np.sin(LT * np.pi / 12) - mag['d20']['dBdMhd'] * np.sin((np.pi/2)-(20 * np.pi / 180)) * np.sin(LT * np.pi/12) + mag['d20']['dBeMhd'] * np.cos(LT*np.pi/12),
                       -mag['d25']['dBnMhd'] * np.cos((np.pi/2)-(25 * np.pi / 180)) * np.sin(LT * np.pi / 12) - mag['d25']['dBdMhd'] * np.sin((np.pi/2)-(25 * np.pi / 180)) * np.sin(LT * np.pi/12) + mag['d25']['dBeMhd'] * np.cos(LT*np.pi/12),
                       -mag['d30']['dBnMhd'] * np.cos((np.pi/2)-(30 * np.pi / 180)) * np.sin(LT * np.pi / 12) - mag['d30']['dBdMhd'] * np.sin((np.pi/2)-(30 * np.pi / 180)) * np.sin(LT * np.pi/12) + mag['d30']['dBeMhd'] * np.cos(LT*np.pi/12),
                       -mag['d35']['dBnMhd'] * np.cos((np.pi/2)-(35 * np.pi / 180)) * np.sin(LT * np.pi / 12) - mag['d35']['dBdMhd'] * np.sin((np.pi/2)-(35 * np.pi / 180)) * np.sin(LT * np.pi/12) + mag['d35']['dBeMhd'] * np.cos(LT*np.pi/12),
                       -mag['d40']['dBnMhd'] * np.cos((np.pi/2)-(40 * np.pi / 180)) * np.sin(LT * np.pi / 12) - mag['d40']['dBdMhd'] * np.sin((np.pi/2)-(40 * np.pi / 180)) * np.sin(LT * np.pi/12) + mag['d40']['dBeMhd'] * np.cos(LT*np.pi/12),
                       -mag['d45']['dBnMhd'] * np.cos((np.pi/2)-(45 * np.pi / 180)) * np.sin(LT * np.pi / 12) - mag['d45']['dBdMhd'] * np.sin((np.pi/2)-(45 * np.pi / 180)) * np.sin(LT * np.pi/12) + mag['d45']['dBeMhd'] * np.cos(LT*np.pi/12),
                       -mag['d50']['dBnMhd'] * np.cos((np.pi/2)-(50 * np.pi / 180)) * np.sin(LT * np.pi / 12) - mag['d50']['dBdMhd'] * np.sin((np.pi/2)-(50 * np.pi / 180)) * np.sin(LT * np.pi/12) + mag['d50']['dBeMhd'] * np.cos(LT*np.pi/12),
                       -mag['d55']['dBnMhd'] * np.cos((np.pi/2)-(55 * np.pi / 180)) * np.sin(LT * np.pi / 12) - mag['d55']['dBdMhd'] * np.sin((np.pi/2)-(55 * np.pi / 180)) * np.sin(LT * np.pi/12) + mag['d55']['dBeMhd'] * np.cos(LT*np.pi/12),
                       -mag['d60']['dBnMhd'] * np.cos((np.pi/2)-(60 * np.pi / 180)) * np.sin(LT * np.pi / 12) - mag['d60']['dBdMhd'] * np.sin((np.pi/2)-(60 * np.pi / 180)) * np.sin(LT * np.pi/12) + mag['d60']['dBeMhd'] * np.cos(LT*np.pi/12),
                       -mag['d65']['dBnMhd'] * np.cos((np.pi/2)-(65 * np.pi / 180)) * np.sin(LT * np.pi / 12) - mag['d65']['dBdMhd'] * np.sin((np.pi/2)-(65 * np.pi / 180)) * np.sin(LT * np.pi/12) + mag['d65']['dBeMhd'] * np.cos(LT*np.pi/12),
                       -mag['d70']['dBnMhd'] * np.cos((np.pi/2)-(70 * np.pi / 180)) * np.sin(LT * np.pi / 12) - mag['d70']['dBdMhd'] * np.sin((np.pi/2)-(70 * np.pi / 180)) * np.sin(LT * np.pi/12) + mag['d70']['dBeMhd'] * np.cos(LT*np.pi/12),
                       -mag['d75']['dBnMhd'] * np.cos((np.pi/2)-(75 * np.pi / 180)) * np.sin(LT * np.pi / 12) - mag['d75']['dBdMhd'] * np.sin((np.pi/2)-(75 * np.pi / 180)) * np.sin(LT * np.pi/12) + mag['d75']['dBeMhd'] * np.cos(LT*np.pi/12),
                       -mag['d80']['dBnMhd'] * np.cos((np.pi/2)-(80 * np.pi / 180)) * np.sin(LT * np.pi / 12) - mag['d80']['dBdMhd'] * np.sin((np.pi/2)-(80 * np.pi / 180)) * np.sin(LT * np.pi/12) + mag['d80']['dBeMhd'] * np.cos(LT*np.pi/12)])

    mhd[2] = np.array([mag['d10']['dBnMhd'] * np.sin((np.pi/2)-(10 * np.pi / 180)) - mag['d10']['dBdMhd'] * np.cos((np.pi/2)-(10 * np.pi / 180)),
                       mag['d15']['dBnMhd'] * np.sin((np.pi/2)-(15 * np.pi / 180)) - mag['d15']['dBdMhd'] * np.cos((np.pi/2)-(15 * np.pi / 180)),
                       mag['d20']['dBnMhd'] * np.sin((np.pi/2)-(20 * np.pi / 180)) - mag['d20']['dBdMhd'] * np.cos((np.pi/2)-(20 * np.pi / 180)),
                       mag['d25']['dBnMhd'] * np.sin((np.pi/2)-(25 * np.pi / 180)) - mag['d25']['dBdMhd'] * np.cos((np.pi/2)-(25 * np.pi / 180)),
                       mag['d30']['dBnMhd'] * np.sin((np.pi/2)-(30 * np.pi / 180)) - mag['d30']['dBdMhd'] * np.cos((np.pi/2)-(30 * np.pi / 180)),
                       mag['d35']['dBnMhd'] * np.sin((np.pi/2)-(35 * np.pi / 180)) - mag['d35']['dBdMhd'] * np.cos((np.pi/2)-(35 * np.pi / 180)),
                       mag['d40']['dBnMhd'] * np.sin((np.pi/2)-(40 * np.pi / 180)) - mag['d40']['dBdMhd'] * np.cos((np.pi/2)-(40 * np.pi / 180)),
                       mag['d45']['dBnMhd'] * np.sin((np.pi/2)-(45 * np.pi / 180)) - mag['d45']['dBdMhd'] * np.cos((np.pi/2)-(45 * np.pi / 180)),
                       mag['d50']['dBnMhd'] * np.sin((np.pi/2)-(50 * np.pi / 180)) - mag['d50']['dBdMhd'] * np.cos((np.pi/2)-(50 * np.pi / 180)),
                       mag['d55']['dBnMhd'] * np.sin((np.pi/2)-(55 * np.pi / 180)) - mag['d55']['dBdMhd'] * np.cos((np.pi/2)-(55 * np.pi / 180)),
                       mag['d60']['dBnMhd'] * np.sin((np.pi/2)-(60 * np.pi / 180)) - mag['d60']['dBdMhd'] * np.cos((np.pi/2)-(60 * np.pi / 180)),
                       mag['d65']['dBnMhd'] * np.sin((np.pi/2)-(65 * np.pi / 180)) - mag['d65']['dBdMhd'] * np.cos((np.pi/2)-(65 * np.pi / 180)),
                       mag['d70']['dBnMhd'] * np.sin((np.pi/2)-(70 * np.pi / 180)) - mag['d70']['dBdMhd'] * np.cos((np.pi/2)-(70 * np.pi / 180)),
                       mag['d75']['dBnMhd'] * np.sin((np.pi/2)-(75 * np.pi / 180)) - mag['d75']['dBdMhd'] * np.cos((np.pi/2)-(75 * np.pi / 180)),
                       mag['d80']['dBnMhd'] * np.sin((np.pi/2)-(80 * np.pi / 180)) - mag['d80']['dBdMhd'] * np.cos((np.pi/2)-(80 * np.pi / 180)),])
    
    return t, mhd

LT00 = mhd('SWMF/run_test/GM/IO2/magnetometers_e20150321-054500.mag')


custom_lines = [Line2D([0], [0], color='#ff6961', lw=1)]

style()

start = LT00[0]
end = start + timedelta(seconds = 5)

for number in range(281):
    fig, ax = plt.subplots()
    for num, item in enumerate(LT00[1][1]):
        ax.plot(LT00[0], LT00[1][2][num], color = '#ff6961')

    frame = datetime(2015, 3, 21, 5, 58, 20) + timedelta(seconds = number)
    box = plt.gca().get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    #ax.legend(custom_lines, ['LT00', 'LT03', 'LT06', 'LT09', 'LT12', 'LT15', 'LT18', 'LT21'], loc='center left', bbox_to_anchor=(1, 0.5), frameon = True)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.axvline(x = frame, linestyle = 'dotted', color = 'black')
    plt.ylim(-75, 320)
    #plt.xlim(start, end)
    plt.xticks(np.arange(datetime(2015, 3, 21, 5, 58, 00), datetime(2015, 3, 21, 6, 3, 0), timedelta(minutes = 1)).astype(datetime))
    plt.title(r'$B_z \ vs. \ UT$'+'\n'+f"{frame.hour:02}"+':'+f"{frame.minute:02}"+':'+f"{frame.second:02}")
    plt.ylabel(r'$B_z \ (nT)$')
    plt.xlabel('UT (HH:MM)')
    plt.tick_params(rotation=45)
    #plt.savefig('test2/'+f"{frame.hour:02}"+f"{frame.minute:02}"+f"{frame.second:02}"+'.png', bbox_inches='tight')
    plt.show()
