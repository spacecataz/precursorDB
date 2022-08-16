import matplotlib.pyplot as plt
from glob import glob
from spacepy.pybats import IdlFile
from spacepy.pybats.bats import MagGridFile, Bats2d

# Path to out files
path = 'SWMF/run_test/GM/IO2/'
savloc = 'test4/'

files = glob(path + 'z=0*.out')
files.sort(key = str)

def Bfield(file):
    mhd = Bats2d(file)
    mhd.add_contour('x','y','by', filled=False)
    plt.savefig(savloc+file[-14:-9]+'.png')
    plt.close()


'''
# Use subclasses to get output-specific functionality:
mhd1 = Bats2d(path + 'z=0_mhd_2_e20150321-060600-000.out')

#fig,ax=mhd1.add_grid_plot()
mhd1.add_contour('x','y','by', filled=False)

plt.show()
'''
for item in files:
    Bfield(item)
