import numpy as np
import matplotlib.pyplot as plt

from skimage import data, draw
from skimage.registration import phase_cross_correlation
from scipy import ndimage as ndi
image = data.camera()
shift = (-22, 13)

corrupted_pixels = np.random.choice([False, True], size=image.shape,
                                    p=[0.25, 0.75])

# The shift corresponds to the pixel offset relative to the reference image
offset_image = ndi.shift(image, shift)
offset_image *= corrupted_pixels
print(f"Known offset (row, col): {shift}")

# Determine what the mask is based on which pixels are invalid
# In this case, we know what the mask should be since we corrupted
# the pixels ourselves
mask = corrupted_pixels

import cv2
import numpy as np
img1 = np.float32(cv2.imread("xNFfw.png",2))
img2 = np.float32(cv2.imread("xNFfw1.png",2))
#r"C:\Users\NSFW\source\repos\CameraMovingDetection\CameraMovingDetection\datasets\xNFfw.png"

detected_shift = phase_cross_correlation(image, offset_image,
                                         reference_mask=mask)

print(f"Detected pixel offset (row, col): {-detected_shift}")

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharex=True, sharey=True,
                                    figsize=(8, 3))

ax1.imshow(image, cmap='gray')
ax1.set_axis_off()
ax1.set_title('Reference image')

ax2.imshow(offset_image.real, cmap='gray')
ax2.set_axis_off()
ax2.set_title('Corrupted, offset image')

ax3.imshow(mask, cmap='gray')
ax3.set_axis_off()
ax3.set_title('Masked pixels')


plt.show()