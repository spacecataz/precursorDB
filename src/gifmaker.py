import imageio
from glob import glob

loc = 'test/'

frames = glob(loc + '*.png')
frames.sort(key = str)

with imageio.get_writer('precursorDB/test.gif', mode='I') as writer:
    for frame in frames:
        image = imageio.imread(frame)
        writer.append_data(image)