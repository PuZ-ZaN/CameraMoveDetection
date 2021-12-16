from imutils.video import VideoStream		#read frames from source
from math import sqrt						#calc change vector
import numpy as np							#frame format
import time									#calc fps, elapsed time, etc.
import cv2									#using phaseCorrelate func
import requests								#call url when camera is moving(-ed)
import traceback
from datetime import datetime
import sys
from .History import History

def CalculatePhaseCorrelate(name = "", source = "", callbackUrl="/callback", err_list = {}, host_id = '', host_pulse = {}, isMovedBorder = 100, isMovingBorder = 100, etalonChangeEveryNFps = 500, etalonHistoryLen=50, staticHistoryLen=700,framesBeforeTrigger=10):
	
	try:
		camera = VideoStream(source).start()
		time.sleep(1.0)

		prev_gray = None
		prevGrayStatic = None
		fpsCounter = 0
		_secs_counter = 0
		elapsedSecs = 0
		pEtalonHistory = History(etalonHistoryLen)
		pStaticHistory = History(staticHistoryLen)
		pEtalonAvg = 0
		pStaticAvg = 0
		_prev_time = time.time()
		frame = None
		imGray = None
		vectorPEtalon = None
		vectorPStatic = None

		prevFrames=[]
		prefFramesCounter=0

		while (True):
			try:
				frame = camera.read()#grab the frame from the threaded video file stream
				if(frame is None):
					break

				#save prev N frames
				#if prefFramesCounter<framesBeforeTrigger:
				#	prevFrames[prefFramesCounter] = frame
				#	prefFramesCounter+=1
				#else:
				#	prefFramesCounter=0;

				imGray = cv2.cvtColor(frame.astype('float32'), cv2.COLOR_BGR2GRAY)#convert it to grayscale (while still retaining 3 channels)

				if(prev_gray is None):
					prev_gray = imGray

				if(prevGrayStatic is None):
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
			

				thisTime = time.time()
				_diffTime = thisTime - _prev_time
				_secs_counter +=_diffTime
				_prev_time = thisTime

				if _diffTime != 0.0:
					elapsedSecs = round(1 / _diffTime,2)
				else:
					elapsedSecs = 0

				IsMoving = pEtalonAvg > isMovingBorder
				IsMoved = pStaticAvg > isMovedBorder
				host_pulse[host_id] = f"{str(datetime.now())} :: frames elapsed - {fpsCounter} :: elapsed secs - {elapsedSecs} :: pEthalon - {pEtalonAvg} :: pStatic - {pStaticAvg}"
				if (IsMoving or IsMoved):
					r = requests.post(r"http://localhost:5555/callback",data={ #TODO Починить гавно
						'name' : str(name),
						'timestamp': str(thisTime),
						'elapsedSecs':str(elapsedSecs),
						'IsMoving':str(IsMoving),
						'IsMoved':str(IsMoved),
						#'prevFrames' : prevFrames, 
						#'frame':frame
						})

			except Exception as e:
				err_list[host_id] = traceback.format_exc()
				break

		camera.stop()
		err_list[host_id] = f'success finish {fpsCounter}'
	except Exception as e:
		err_list[host_id] = traceback.format_exc()