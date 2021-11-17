import matplotlib.pyplot as plt
plt.ion()
class DynamicPlot():
	min_x = 0
	max_x = 10
	xdata = []
	ydata1 = []
	ydata2 = []
	FirstLine = None
	SecondLine = None
	ax = None
	figure = None

	def __init__(self,ylabel='Vector Changes Lenght', xlabel='Frames/3',suptitle='Image Change Speed',cursor="-"):
		self.figure, self.ax = plt.subplots()
		self.figure.suptitle(suptitle, fontsize=20)
		plt.xlabel(xlabel, fontsize=18)
		plt.ylabel(ylabel, fontsize=16)
		self.FirstLine, = self.ax.plot([], [], cursor, label = "Static")
		self.SecondLine, = self.ax.plot([], [], cursor, label = "Etalon")
		self.ax.set_autoscaley_on(True)
		self.ax.set_xlim(self.min_x, self.max_x)
		self.ax.legend(loc='upper left')
		self.ax.grid()

	def addPoint(self,x,y1,y2):
		self.xdata.append(x)
		self.ydata1.append(y1)		
		self.ydata2.append(y2)
		self.FirstLine.set_xdata(self.xdata)
		self.FirstLine.set_ydata(self.ydata1)
		self.SecondLine.set_xdata(self.xdata)
		self.SecondLine.set_ydata(self.ydata2)
		
		if(x > self.max_x):
			self.max_x = x * 1.5
		#Need both of these in order to rescale
		self.ax.set_xlim(self.min_x, self.max_x)
		self.ax.relim()
		self.ax.autoscale_view()
		#We need to draw *and* flush
		self.figure.canvas.draw()
		self.figure.canvas.flush_events()