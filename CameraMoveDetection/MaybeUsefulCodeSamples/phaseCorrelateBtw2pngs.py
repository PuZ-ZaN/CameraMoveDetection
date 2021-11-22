raise Exception("Not for run!")

#Сравнить 2 png
import cv2
import numpy as np
img1 = np.float32(cv2.imread("datasets/xNFfw.png",2))
img2 = np.float32(cv2.imread("datasets/xNFfw1.png",2))
print(cv2.phaseCorrelate(img1,img2))