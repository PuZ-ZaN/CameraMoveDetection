from imutils.video import FileVideoStream
#from imutils.video import FPS
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
import imutils
import time
import cv2
from DynamicPlot import DynamicPlot

def turpleRound(turple):
	res = []
	for i in turple:
		if type(i) is tuple:
			res.append(turpleRound(i))
		else:
			res.append(round(i,2))
	return res

def takeFirstFrameAsEtalon(filename):
	cap = cv2.VideoCapture(filename)
	#take first frame
	ret, im = cap.read()
	im = im.astype('float32')
	prev_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	return prev_gray

def main():
	isMovedBorder=400
	isMovingBorder=100
	etalonChangeEveryNFps=500
	filename = "datasets/g.mp4"


	fvs = FileVideoStream(filename).start()
	time.sleep(1.0)
	prev_gray = takeFirstFrameAsEtalon(filename)
	prevGrayStatic=prev_gray
	fpsCounter = 0
	start_time = time.time()
	secs_counter=0
	while fvs.more():
		try:
			
			
			frame = fvs.read()#grab the frame from the threaded video file stream
			imGray = cv2.cvtColor(frame.astype('float32'), cv2.COLOR_BGR2GRAY)#convert it to grayscale (while still retaining 3 channels)
			pEtalon = cv2.phaseCorrelate(imGray, prev_gray)
			pStatic = cv2.phaseCorrelate(imGray,prevGrayStatic)
			#cv2.putText(frame, "phaseCorrelateEtalon: {}".format(turpleRound(pEtalon)), (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
			
			thisTime=time.time()
			diffTime = thisTime - start_time
			secs_counter +=diffTime

			fpsCounter+=1
			if fpsCounter % etalonChangeEveryNFps == 0:
				prev_gray = imGray

			vectorChange = sqrt(pEtalon[0][0] ** 2 + pEtalon[0][1] ** 2)
			vectorChangeStatic = sqrt(pStatic[0][0] ** 2 + pStatic[0][1] ** 2)
			
			start_time=thisTime

			colorMoving = (0, 255, 0)
			colorMoved = (0, 255, 0)
			IsMoving = vectorChange>isMovingBorder
			IsMoved = vectorChangeStatic>isMovedBorder
			if(IsMoving):
				colorMoving = (0, 0, 255)
			if(IsMoved):
				colorMoved = (0, 0, 255)
			
			
			cv2.putText(frame, "Fps: {}".format(round(1/diffTime,2)), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
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

			
			#fps.update()
		except Exception as e:
			print("ERROR:")
			print(e)
			break
	# stop the timer and display FPS information
	#fps.stop()
	#print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
	#print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
	#cleanup
	cv2.destroyAllWindows()
	fvs.stop()

if __name__ == '__main__':
	main()




#
# def CorrelationDifference(correlation1, correlation2):
# 	if type(correlation1)!=type(correlation2):
# 		raise Exception("types mismatch")
# 	res = []
# 	for i in zip (correlation1, correlation2):
# 		if not ((type(i[0]) is tuple) or (type(i[0] is list))):
# 			res.append(abs(abs(i[0])-abs(i[1])))
# 		else:
# 			res.append(CorrelationDifference(i[0],i[1]))
# 	return res

#from main:
# grab the frame from the threaded video file stream, resize it, and convert it to grayscale (while still retaining 3 channels)
# frame = imutils.resize(frame, width=450)
# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# frame = np.dstack([frame, frame, frame])
# display the size of the queue on the frame
# cv2.putText(frame, "Queue Size: {}".format(fvs.Q.qsize()),
# (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
# show the frame and update the FPS counter

# 	print ("Warning sec:" + str (counter / realFps))
# if(p>prev)
# 	counter += 1
# etalonCortage = ((0.7, 0.4), 0.7)
#prev_frame = cv2.cvtColor (im, cv2.COLOR_BGR2GRAY)
#counter = 0
#realFps = cap.get (cv2.CAP_PROP_FPS)


#if move is None:
#	move = (-p[0][0], -p[0][1])
#else:
#	move = ( move[0] - p[0][0], move[1] - p[0][1])	
#points.append(move)
#xp = []
#yp = []
#for p in points:
#	xp.append(p[1])
#	yp.append(p[0])

#plt.figure(2)
#line = plt.plot(yp,xp)
#plt.xlabel('Horizontal Movement')
#plt.ylabel('Vertical Movement')
#plt.title('Phase Correlation Movement, x-y plot')
#plt.annotate('Start', xy=(0, 0), xytext=(-20, 400),arrowprops=dict(facecolor='black', shrink=0.05))
#plt.show()

#plt.figure(0)
#line = plt.plot(points)
#plt.legend()#line, ('Horizontal', 'Vertical'), 'best'
#plt.xlabel('Frame')
#plt.ylabel('Movement')
#plt.title('Phase Correlation Movement')
##plt.show(block=False)
#plt.draw()
#plt.pause(0.1)
#plt.close()

#exit if key pressed