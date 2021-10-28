import cv2
import numpy as np
# Создаем объект захвата видео, в этом случае мы читаем видео из файла
vid_capture = cv2.VideoCapture ('seVidTest.mp4')
imgPrev=np.ones((480, 852, 3))#np.ndarray((480, 852, 3))
frame=np.ones((480, 852, 3))#np.ndarray((480, 852, 3))
if (vid_capture.isOpened () == False):
	print ("Ошибка открытия видеофайла")
# Чтение fps и количества кадров
else:
	# Получить информацию о частоте кадров
	# Можно заменить 5 на CAP_PROP_FPS, это перечисления
	fps = vid_capture.get (5)
	print ('Фреймов в секунду: ', fps, 'FPS')
	# Получить количество кадров
	# Можно заменить 7 на CAP_PROP_FRAME_COUNT, это перечисления
	frame_count = vid_capture.get (7)
	print ('Частота кадров: ', frame_count)
	print ('\n-----------------------------\nДля завершения нажмите "q" или Esc...')
file_count = 0
while (vid_capture.isOpened ()):
	# Метод vid_capture.read() возвращают кортеж, первым элементом является логическое значение
	# а вторым кадр
	ret, frame = vid_capture.read ()
	if ret == True:
		cv2.imshow ('Look', frame)
		file_count += 1
		print ('Кадр {0:04d}'.format (file_count))
		# writefile = 'Resources/Image_sequence/is42_{0:04d}.jpg'.format(file_count)
		# cv2.imwrite(writefile, frame)
		# 20 в миллисекундах, попробуйте увеличить значение, скажем, 50 и
		# понаблюдайте за изменениями в показе
		try:
			imgCurrent = np.float32(frame.astype("float32")/255)
			img
			print(type(imgCurrent))
			print(type(imgPrev))
			if(type(imgCurrent) == type(imgPrev)):
				print(cv2.phaseCorrelate (imgCurrent, imgCurrent.copy()))
			imgPrev = imgCurrent
		except Exception as e:
			print(e)
			vid_capture.release()
			cv2.destroyAllWindows()
			
		key = cv2.waitKey (20)

		if (key == ord ('q')) or key == 27:
			break
	else:
		break

# Освободить объект захвата видео
vid_capture.release ()
cv2.destroyAllWindows ()