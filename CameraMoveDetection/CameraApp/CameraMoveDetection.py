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
#from .SmartThreadPool import ThreadSafeDict
"""
Считает 2 вектора смещения камеры: относительно эталона и static'а
Эталон - смещаемый каждые N кадров кадр
Static - не меняется, первый кадр видео
"""
def CalculatePhaseCorrelate(CameraID = "", 
							Url = "", 
							IsMovedBorder = 100, 
							IsMovingBorder = 100, 
							callbackUrl=r"http://localhost:5555/SignalAdd",
							sendImageUrl=r"http://localhost:5555/SendImage",
							etalonChangeEveryNFps = 500, 
							ServerUpdateNFrames = 10,
							etalonHistoryLen=50, 
							staticHistoryLen=700,
							err_list = {}, 
							host_id = '', 
							host_pulse = {}, 
							):
	try:
		print(f"BEBIN {CameraID} {Url}")
		camera = VideoStream(Url).start()
		#time.sleep(1.0) #задержка, возможно она не нужна
		prev_gray = None
		prevGrayStatic = None
		fpsCounter = 0
		#_secs_counter = 0
		#elapsedSecs = 0
		pEtalonHistory = History(etalonHistoryLen)
		pStaticHistory = History(staticHistoryLen)
		pEtalonAvg = 0
		pStaticAvg = 0
		#_prev_time = time.time()
		Frame = None
		imGray = None
		vectorPEtalon = None
		vectorPStatic = None
		while (True):
			try:
				#возьмем кадр
				Frame = camera.read()
				if(Frame is None):
					break

				if(fpsCounter%ServerUpdateNFrames==0):
					retval, buffer = cv2.imencode('.jpg', Frame)
					jpg_as_text = "data:image/jpeg;base64,"+str(base64.b64encode(buffer))
					requests.post(sendImageUrl,data={
						'CameraID' : CameraID,
						'Frame':jpg_as_text,
						"pStaticAvg":pEtalonAvg,
						"pEtalonAvg":pStaticAvg
						})
				
				#конвертнем в серый
				imGray = cv2.cvtColor(Frame.astype('float32'), cv2.COLOR_BGR2GRAY)

				if(prev_gray is None):
					prev_gray = imGray

				if(prevGrayStatic is None):
					prevGrayStatic=imGray

				#Вычислим средние значения векторов смещения за HistoryLen (см. агрументы) кадров
				pEtalon = cv2.phaseCorrelate(imGray, prev_gray)
				pStatic = cv2.phaseCorrelate(imGray,prevGrayStatic)
				vectorPEtalon = sqrt(pEtalon[0][0] ** 2 + pEtalon[0][1] ** 2)
				vectorPStatic = sqrt(pStatic[0][0] ** 2 + pStatic[0][1] ** 2)
				pEtalonHistory.append(vectorPEtalon)
				pStaticHistory.append(vectorPStatic)
				pEtalonAvg = pEtalonHistory.avgCalc()
				pStaticAvg = pStaticHistory.avgCalc()
				
				#host_pulse[host_id]=f"fpsCounter: {fpsCounter} Etalon:{pEtalonAvg} Static:{pStaticAvg}"
				#Обновим эталонный кадр каждые N fps (см. агрументы)
				fpsCounter+=1
				if etalonChangeEveryNFps!=0 and fpsCounter % etalonChangeEveryNFps == 0:
					prev_gray = imGray

				#вычислим fps
				#thisTime = time.time()
				#_diffTime = thisTime - _prev_time
				#_secs_counter +=_diffTime
				#_prev_time = thisTime

				#if _diffTime != 0.0:
				#	elapsedSecs += round(1 / _diffTime,2)

				IsMoving = pEtalonAvg > IsMovingBorder
				IsMoved = pStaticAvg > IsMovedBorder
				if (IsMoving or IsMoved):
					print("SEE BD")
					retval, buffer = cv2.imencode('.jpg', Frame)
					jpg_as_text = base64.b64encode(buffer)
					r = requests.post(callbackUrl,data={
						'CameraID' : CameraID,
						'TimeStamp': str(thisTime),
						'IsMoving':str(IsMoving),
						'IsMoved':str(IsMoved),
						'Frame':jpg_as_text
						})
					print("SEE DATABASE SIGNALS!!!")
					err_list[host_id] = f"CameraID {CameraID} saying {r}"
			except Exception as e:
				err_list[host_id] = e#traceback.format_exc()
				print("FUCKING SLAVS")
				print(str(e))
				break

		camera.stop()
		err_list[host_id] = f'success finish {fpsCounter}'
	except Exception as e:
		err_list[host_id] = e#traceback.format_exc()
		print(str(e))
	err_list[host_id] = "End"
	print("END")