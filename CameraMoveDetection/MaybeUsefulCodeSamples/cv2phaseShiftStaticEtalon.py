#!/usr/bin/env python
import cv2
import numpy
import operator
import matplotlib.pyplot as plt
import sys, os

def main(showvid=False):
	try:
		filename = "g.mp4"  # getFileName()
		cap = cv2.VideoCapture (filename)
		realFps = cap.get(cv2.CAP_PROP_FPS)
		ret, im = cap.read ()
		im = im.astype ('float32')
		prev_gray = cv2.cvtColor (im, cv2.COLOR_BGR2GRAY)
		move = None
		points = []
		counter=0
		maxp = ((0,0),0)
		maxpOnFrame=0
		etalonCortage = ((0.7, 0.4), 0.7)
		while True:
			ret, im = cap.read ()
			if ret is False:
				break
			imf32 = im.astype ('float32')
			imGray = cv2.cvtColor (imf32, cv2.COLOR_BGR2GRAY)
			p = cv2.phaseCorrelate (imGray, prev_gray)
			prev_gray = imGray
			if(showvid):
				#print ("frame"+str(counter))
				#print (p)
				cv2.imshow ('Look', im)
				if(
						abs(p[0][0])>etalonCortage[0][0] and
						abs(p[0][1])>etalonCortage[0][1] and
						abs(p[1])>etalonCortage[1]
				):
					print("Warning sec:" + str(counter/realFps))
			else:
				print ("Pulse " + str (counter))
			# if(p[0] > maxp[0]):
			# 	maxp = p
			# 	maxpOnFrame = counter
			counter += 1
			key = cv2.waitKey (20)
			if (key == ord ('q')) or key == 27:
				print("exit..")
				break
	except Exception as e:
		print(e)
	finally:
		cap.release ()
		cv2.destroyAllWindows ()
		print("clean")
		print("MaxP = "+str(maxp))
		print("MaxP on Frame"+str(maxpOnFrame))

if __name__ == '__main__':
	main (True)
		# P is movement form top left = (0,0), so need to invert all numbers
		# if move is None:
		# 	move = (-p[0], -p[1])
		# else:
		# 	move = ( move[0] - p[0], move[1] - p[1])
		# print(move)
		# points.append(move)
		# print 'Total move: ', move
	# plt.figure (1)
	# line = plt.plot (points)
	# plt.legend (line, ('Horizontal', 'Vertical'), 'best')
	# plt.xlabel ('Frame')
	# plt.ylabel ('Movement')
	# plt.title ('Phase Correlation Movement')
	#
	# xp = []
	# yp = []
	# for p in points:
	# 	xp.append (p[1])
	# 	yp.append (p[0])
	#
	# plt.figure (2)
	# line = plt.plot (yp, xp)
	# plt.xlabel ('Horizontal Movement')
	# plt.ylabel ('Vertical Movement')
	# plt.title ('Phase Correlation Movement, x-y plot')
	# plt.annotate ('Start', xy=(0, 0), xytext=(-20, 400), arrowprops=dict (facecolor='black', shrink=0.05))
	# plt.show ()

	#время от времени нужно сравнивать с группой кадров с минимальными изменениями
