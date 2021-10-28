# import the necessary packages
from imutils.video import FileVideoStream
from imutils.video import FPS
import numpy as np
import imutils
import time
import cv2

def turpleRound(turple):
	res = []
	for i in turple:
		if type(i) is tuple:
			res.append (turpleRound(i))
		else:
			res.append(round(i,2))
	return res

def main():
	filename = "g.mp4"
	fvs = FileVideoStream (filename).start ()
	time.sleep (1.0)
	# start the FPS timer
	fps = FPS ().start ()
	cap = cv2.VideoCapture (filename)

	#take first frame
	ret, im = cap.read ()
	im = im.astype ('float32')
	prev_gray = cv2.cvtColor (im, cv2.COLOR_BGR2GRAY)
	lastFrameGray = prev_gray
	# loop over frames from the video file stream
	while fvs.more ():
		try:
			frame = fvs.read ()#grab the frame from the threaded video file stream
			imf32 = frame.astype ('float32')
			imGray = cv2.cvtColor (imf32, cv2.COLOR_BGR2GRAY)#convert it to grayscale (while still retaining 3 channels)
			pEtalon = cv2.phaseCorrelate (imGray, prev_gray)
			p2Frames = cv2.phaseCorrelate (imGray, lastFrameGray)
			lastFrameGray = imGray

			cv2.putText (frame, "phaseCorrelateEtalon: {}".format (turpleRound(pEtalon)), (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
			cv2.putText (frame, "phaseCorrelateBtw2Frames: {}".format (turpleRound(p2Frames)), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)


			cv2.imshow ("Frame", frame)
			# cv2.putText (imGray, "phaseCorrelateEtalon: {}".format (turpleRound (pEtalon)), (20, 30),
			#              cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
			# cv2.putText (imGray, "phaseCorrelateBtw2Frames: {}".format (turpleRound (p2Frames)), (20, 60),
			#              cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
			# cv2.imshow ("FrameGray",imGray)


			#exit if key pressed
			key = cv2.waitKey (20)
			if (key == ord ('q')) or key == 27:
				print ("exit..")
				break
			cv2.waitKey (1)
			fps.update ()
		except Exception as e:
			print("ERROR:")
			print(e)
			break
	# stop the timer and display FPS information
	fps.stop ()
	print ("[INFO] elasped time: {:.2f}".format (fps.elapsed ()))
	print ("[INFO] approx. FPS: {:.2f}".format (fps.fps ()))
	#cleanup
	cv2.destroyAllWindows ()
	fvs.stop ()

if __name__ == '__main__':
	main ()




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