from imutils.video import FileVideoStream
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
import imutils
import time
import cv2

def takeFirstFrameAsEtalon(filename):
	cap = cv2.VideoCapture(filename)
	ret, im = cap.read()
	im = im.astype('float32')
	prev_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	return prev_gray

def main():
	isMovedBorder = 400
	isMovingBorder = 100
	etalonChangeEveryNFps = 500
	filename = "datasets/g.mp4"

	fvs = FileVideoStream(filename).start()
	time.sleep(1.0)
	prev_gray = takeFirstFrameAsEtalon(filename)
	prevGrayStatic = prev_gray
	fpsCounter = 0
	start_time = time.time()
	secs_counter = 0
	while fvs.more():
		try:
			frame = fvs.read()#grab the frame from the threaded video file stream
			imGray = cv2.cvtColor(frame.astype('float32'), cv2.COLOR_BGR2GRAY)#convert it to grayscale (while still retaining 3 channels)
			pEtalon = cv2.phaseCorrelate(imGray, prev_gray)
			pStatic = cv2.phaseCorrelate(imGray,prevGrayStatic)
			#cv2.putText(frame, "phaseCorrelateEtalon: {}".format(turpleRound(pEtalon)),
			#(20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
			
			thisTime = time.time()
			diffTime = thisTime - start_time
			secs_counter +=diffTime

			fpsCounter+=1
			if fpsCounter % etalonChangeEveryNFps == 0:
				prev_gray = imGray

			vectorChange = sqrt(pEtalon[0][0] ** 2 + pEtalon[0][1] ** 2)
			vectorChangeStatic = sqrt(pStatic[0][0] ** 2 + pStatic[0][1] ** 2)
			
			start_time = thisTime

			colorMoving = (0, 255, 0)
			colorMoved = (0, 255, 0)
			IsMoving = vectorChange > isMovingBorder
			IsMoved = vectorChangeStatic > isMovedBorder
			if(IsMoving):
				colorMoving = (0, 0, 255)
			if(IsMoved):
				colorMoved = (0, 0, 255)
			
			cv2.putText(frame, "Fps: {}".format(round(1 / diffTime,2)), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
			cv2.putText(frame, "secs_counter: {}s".format(round(secs_counter,1)), (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
			cv2.putText(frame, "IsMoving: {}".format(IsMoving), (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, colorMoving, 2)
			cv2.putText(frame, "IsMovingVecLen: {}".format(vectorChange), (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
			cv2.putText(frame, "IsMoved: {}".format(IsMoved), (20, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.6, colorMoved, 2)
			cv2.putText(frame, "IsMovedVecLen: {}".format(vectorChangeStatic), (20, 210), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
			cv2.putText(frame, "IsMovedBorder: {}".format(isMovedBorder), (20, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
			cv2.putText(frame, "IsMovingBorder: {}".format(isMovingBorder), (20, 280), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
			cv2.imshow("Frame", frame)
			
			key = cv2.waitKey(1)
			if key == 27 or key == ord('q'):
				print("exit..")
				break
		except Exception as e:
			print("ERROR:")
			print(e)
			break
	cv2.destroyAllWindows()
	fvs.stop()

if __name__ == '__main__':
	main()