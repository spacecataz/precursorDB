
import cv2
import os

image_folder = 'test5/'
video_name = 'centeredSSI.mp4'

images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
images.sort(key=str)
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(video_name, fourcc, 10, (width,height))

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()
'''

import imageio
import os

image_folder = 'precursorDB/docs/EventList/SEA/ideal_ssc/LT_Analysis/combined/'
images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
images.sort(key=str)


with imageio.get_writer('test.mp4', mode='I') as writer:
    for image in images:
        image = imageio.imread(os.path.join(image_folder, image))
        writer.append_data(image)
'''