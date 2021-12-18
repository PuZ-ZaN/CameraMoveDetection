from imutils.video import FileVideoStream
from math import sqrt
import numpy as np
#import matplotlib.pyplot as plt
import imutils
import time
import cv2

from History import History
#from DynamicPlot import DynamicPlot
from Config import Config
import base64
#from scipy.fftpack import fftn, ifftn
#from aioify import aioify
#import asyncio

#def phase_correlation(a, b):
#	G_a = np.fft.fft2(a)
#	G_b = np.fft.fft2(b)
#	conj_b = np.ma.conjugate(G_b)
#	R = G_a * conj_b
#	R /= np.absolute(R)
#	r = np.fft.ifft2(R).real
#	(x,y) = np.unravel_index(r.argmax(), r.shape)
#	return ((x,y),0)

#def phase_correlation(a, b):
#	r = (ifftn(fftn(a)*ifftn(a))).real
#	(x,y) = np.unravel_index(r.argmax(), r.shape)
#	return ((x,y),0) #результат всегда 0 почемуто
def takeFirstFrameAsEtalon(filename):
	cap = cv2.VideoCapture(filename)
	#im = None #возможно это (и иф ниже) понадобится, если контент в cap окажется
	#не изображением (я не знаю возможно ли это)
	#while im ==None:
	ret, im = cap.read()
		#if(im==None):
			#print("ERR - NONE")
			#continue
	im = im.astype('float32')
	prev_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	return prev_gray

def main():
	print(cv2.getBuildInformation())
	print(np.show_config())
	config = Config()
	print("Settings:")
	print(config.__dict__)

	fvs = FileVideoStream(config.filename).start()
	time.sleep(1.0)
	prev_gray = takeFirstFrameAsEtalon(config.filename)
	prevGrayStatic = prev_gray
	
	fpsCounter = 0
	prev_time = time.time()
	secs_counter = 0

	elapsedSecs = 0

	pEtalonHistory = History(config.etalonHistoryLen)
	pStaticHistory = History(config.staticHistoryLen)
	pEtalonAvg = 0
	pStaticAvg = 0

	#dynamicGraph = DynamicPlot()

	while fvs.more() != None:
		try:
			frame = fvs.read()#grab the frame from the threaded video file stream
			if(frame is None):
				break
			#Calculate functionality
			imGray = cv2.cvtColor(frame.astype('float32'), cv2.COLOR_BGR2GRAY)#convert it to grayscale (while still retaining 3 channels)

			pEtalon = cv2.phaseCorrelate(imGray, prev_gray)
			pStatic = cv2.phaseCorrelate(imGray,prevGrayStatic)

			#pEtalon = phase_correlation(imGray, prev_gray)
			#pStatic = phase_correlation(imGray,prevGrayStatic)
			
			vectorPEtalon = sqrt(pEtalon[0][0] ** 2 + pEtalon[0][1] ** 2)
			vectorPStatic = sqrt(pStatic[0][0] ** 2 + pStatic[0][1] ** 2)

			pEtalonHistory.append(vectorPEtalon)
			pStaticHistory.append(vectorPStatic)

			pEtalonAvg = pEtalonHistory.avgCalc()
			pStaticAvg = pStaticHistory.avgCalc()
				
			#gray update functionality
			fpsCounter+=1
			if fpsCounter % config.etalonChangeEveryNFps == 0:
				prev_gray = imGray
			
			#dynamicGraph.addPoint(fpsCounter / 3,pStaticAvg,pEtalonAvg)

			#cv2.putText(frame, "phaseCorrelateEtalon:
			#{}".format(turpleRound(pEtalon)),
			#(20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

			if(config.ShowVideo):
				#fps meter functionality
				thisTime = time.time()
				diffTime = thisTime - prev_time
				secs_counter +=diffTime
				prev_time = thisTime
				elapsedSecs = round(1 / diffTime,2)
				#interface functionality
				#colorMoving = (0, 255, 0)
				#colorMoved = (0, 255, 0)
				#IsMoving = vectorPEtalon > config.isMovingBorder
				#IsMoved = vectorPStatic > config.isMovedBorder
				#if(IsMoving):
				#	colorMoving = (0, 0, 255)
				#if(IsMoved):
				#	colorMoved = (0, 0, 255)

				#avgs colors
				colorPEtalonAvg = (0, 255, 0)
				colorPStaticAvg = (0, 255, 0)
				if(pEtalonAvg > config.isMovingBorder):
					colorPEtalonAvg = (0, 0, 255)
				if(pStaticAvg > config.isMovedBorder):
					colorPStaticAvg = (0, 0, 255)
			
				cv2.putText(frame, "Fps: {}".format(elapsedSecs), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
				cv2.putText(frame, "secs_counter: {}s".format(round(secs_counter,1)), (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

				#cv2.putText(frame, "IsMoving: {}".format(IsMoving), (20, 70),
				#cv2.FONT_HERSHEY_SIMPLEX, 0.6, colorMoving, 2)
				#cv2.putText(frame, "IsMovingVecLen: {}".format(vectorPEtalon), (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
				#cv2.putText(frame, "IsMovingVecsAvg (pEtalonAvg): {}".format(pEtalonAvg), (20, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, colorPEtalonAvg, 2)

				#cv2.putText(frame, "IsMoved: {}".format(IsMoved), (20, 130),
				#cv2.FONT_HERSHEY_SIMPLEX, 0.6, colorMoved, 2)
				#cv2.putText(frame, "IsMovedVecLen: {}".format(vectorPStatic), (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
				#cv2.putText(frame, "IsMovedVecsAvg (pStaticAvg): {}".format(pStaticAvg), (20, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.6, colorPStaticAvg, 2)

				#cv2.putText(frame, "IsMovedBorder: {}".format(config.isMovedBorder), (20, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
				#cv2.putText(frame, "IsMovingBorder: {}".format(config.isMovingBorder), (20, 210), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
				#cv2.putText(frame, "B64: {}".format(stra), (20, 310), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
				
				cv2.imshow(config.NameVideoWindow, frame)
			
			#exit key functionality
			key = cv2.waitKey(1)
			if key == 27 or key == ord('q'):
				print("exit..")
				break
		except Exception as e:
		#	raise e;
			#print("ERROR:")
			print(e)
			break
	fvs.stop()
	#input("Press ENTER key for closing windows")
	#cv2.destroyAllWindows()
	if(config.ShowVideo):
		cv2.destroyWindow(config.NameVideoWindow)

if __name__ == '__main__':
	main()