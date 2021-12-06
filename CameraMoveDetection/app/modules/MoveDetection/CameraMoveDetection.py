from imutils.video import FileVideoStream	#read frames from source
from math import sqrt						#calc change vector
import numpy as np							#frame format
import time									#calc fps, elapsed time, etc.
import cv2									#using phaseCorrelate func
import requests								#call url when camera is moving(-ed)

from . History import History

def CalculatePhaseCorrelate(source = "", callbackUrl="/callback", isMovedBorder = 100, isMovingBorder = 100, etalonChangeEveryNFps = 500, etalonHistoryLen=50, staticHistoryLen=700):
	fvs = FileVideoStream(source).start()
	time.sleep(1.0)

	prev_gray = None
	prevGrayStatic = None
	fpsCounter = 0
	secs_counter = 0
	elapsedSecs = 0
	pEtalonHistory = History(etalonHistoryLen)
	pStaticHistory = History(staticHistoryLen)
	pEtalonAvg = 0
	pStaticAvg = 0
	prev_time = time.time()
	frame = None
	imGray = None
	vectorPEtalon = None
	vectorPStatic = None

	while fvs.more() != None:
		try:
			frame = fvs.read()#grab the frame from the threaded video file stream
			if(frame is None):
				break

			imGray = cv2.cvtColor(frame.astype('float32'), cv2.COLOR_BGR2GRAY)#convert it to grayscale (while still retaining 3 channels)

			if(prev_gray==None):
				prev_gray = imGray

			if(prevGrayStatic==None):
				prevGrayStatic=imGray

			#Calculate functionality

			pEtalon = cv2.phaseCorrelate(imGray, prev_gray)
			pStatic = cv2.phaseCorrelate(imGray,prevGrayStatic)
			vectorPEtalon = sqrt(pEtalon[0][0] ** 2 + pEtalon[0][1] ** 2)
			vectorPStatic = sqrt(pStatic[0][0] ** 2 + pStatic[0][1] ** 2)
			pEtalonHistory.append(vectorPEtalon)
			pStaticHistory.append(vectorPStatic)

			pEtalonAvg = pEtalonHistory.avgCalc()
			pStaticAvg = pStaticHistory.avgCalc()
				
			#gray update functionality
			fpsCounter+=1
			if fpsCounter % etalonChangeEveryNFps == 0:
				prev_gray = imGray
			

			_thisTime = time.time()
			_diffTime = _thisTime - _prev_time
			_secs_counter +=_diffTime
			_prev_time = thisTime

			elapsedSecs = round(1 / _diffTime,2)
			IsMoving = pEtalonAvg > isMovingBorder
			IsMoved = pStaticAvg > isMovedBorder
			
			if (IsMoving or IsMover):
				r = requests.post(callbackUrl,data={'elapsedSecs':elapsedSecs,'IsMoving':IsMoving,'IsMoved':IsMoved})#кадр еще

			key = cv2.waitKey(1)
			if key == 27 or key == ord('q'):
				print("exit..")
				break
		except Exception as e:
			print(e)
			break
	fvs.stop()