import imageio
from glob import glob
from PIL import Image

loc1 = 'test4/'
loc2 = 'test2/'
loc3 = 'test5/'

frames1 = glob(loc1 + '*.png')
frames1.sort(key = str)

frames2 = glob(loc2 + '*.png')
frames2.sort(key = str)

def concat(image1, image2, resample=Image.BICUBIC, resize_big_image=True):
    im1 = Image.open(image2)
    im2 = Image.open(image1)
    if im1.height == im2.height:
        _im1 = im1
        _im2 = im2
    elif (((im1.height > im2.height) and resize_big_image) or
          ((im1.height < im2.height) and not resize_big_image)):
        _im1 = im1.resize((int(im1.width * im2.height / im1.height), im2.height), resample=resample)
        _im2 = im2
    else:
        _im1 = im1
        _im2 = im2.resize((int(im2.width * im1.height / im2.height), im1.height), resample=resample)
    dst = Image.new('RGB', (_im1.width + _im2.width, _im1.height))
    dst.paste(_im1, (0, 0))
    dst.paste(_im2, (_im1.width, 0))
    dst.save(loc3+image2[-10:-4]+'.png')
    return dst

for num in range(len(frames1)):
    concat(frames1[num], frames2[num])
'''

frames3 = glob(loc3 + '*.png')
frames3.sort(key = str)

with imageio.get_writer('precursorDB/test_full.gif', mode='I') as writer:
    for frame in frames3:
        image = imageio.imread(frame)
        writer.append_data(image)
'''