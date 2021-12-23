from imutils.video import VideoStream		#read Frames from Url
from math import sqrt						#calc change vector
import numpy as np							#Frame format
import time									#calc fps, elapsed time, etc.
import cv2									#using phaseCorrelate func
#import requests_async as requests 
import requests								#call url when camera is moving(-ed)
import traceback
from datetime import datetime
import sys
from .History import History
import base64

def CalculatePhaseCorrelate(CameraID = "", Url = "", IsMovedBorder = 100, IsMovingBorder = 100, callbackUrl=r"http://localhost:5555/SignalAdd", err_list = {}, host_id = '', host_pulse = {}, etalonChangeEveryNFps = 500, etalonHistoryLen=50, staticHistoryLen=700):
	try:
		camera = VideoStream(Url).start()
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
		Frame = None
		imGray = None
		vectorPEtalon = None
		vectorPStatic = None
		b=False
		while (True):
			try:
				Frame = camera.read()#grab the Frame from the threaded video file stream
				if(Frame is None):
					break

				imGray = cv2.cvtColor(Frame.astype('float32'), cv2.COLOR_BGR2GRAY)#convert it to grayscale (while still retaining 3 channels)

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
				if etalonChangeEveryNFps!=0 and fpsCounter % etalonChangeEveryNFps == 0:
					prev_gray = imGray
				
				if(b==False):
					b = True
					retval, buffer = cv2.imencode('.jpg', Frame)
					jpg_as_text = base64.b64encode(buffer)
					print(requests.post("http://localhost:5555/NudesSend",data = {"CameraId":CameraID,"Image":jpg_as_text})) 
				#if fpsCounter/10==0:
					

			

				thisTime = time.time()
				_diffTime = thisTime - _prev_time
				_secs_counter +=_diffTime
				_prev_time = thisTime

				if _diffTime != 0.0:
					elapsedSecs = round(1 / _diffTime,2)
				else:
					elapsedSecs = 0

				IsMoving = pEtalonAvg > IsMovingBorder
				IsMoved = pStaticAvg > IsMovedBorder
				host_pulse[host_id] = f"{str(datetime.now())} :: Frames elapsed - {fpsCounter} :: elapsed secs - {elapsedSecs} :: pEthalon - {pEtalonAvg} :: pStatic - {pStaticAvg} :: {Frame}"
				if (IsMoving or IsMoved):
					retval, buffer = cv2.imencode('.jpg', Frame)
					jpg_as_text = base64.b64encode(buffer)
					r = requests.post(callbackUrl,data={
						'CameraID' : CameraID,
						'TimeStamp': str(thisTime),
						'IsMoving':str(IsMoving),
						'IsMoved':str(IsMoved),
						'Frame':jpg_as_text
						})
					err_list[host_id] = f"CameraID {CameraID} saying {r}"
			except Exception as e:
				err_list[host_id] = traceback.format_exc()
				print("FUCKING SLAVS")
				print(traceback.format_exc())
				break

		camera.stop()
		err_list[host_id] = f'success finish {fpsCounter}'
	except Exception as e:
		err_list[host_id] = traceback.format_exc()
	err_list[host_id] = "End"
	print("END")