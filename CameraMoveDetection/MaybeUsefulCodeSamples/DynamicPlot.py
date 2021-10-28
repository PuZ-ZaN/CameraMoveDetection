import matplotlib.pyplot as plt
plt.ion()
class DynamicPlot():
	min_x = 0
	max_x = 10
	xdata = []
	ydata = []
	lines = None
	ax = None
	figure = None

	def __init__(self,ylabel='Vector Changes Lenght', xlabel='Frames',suptitle='Image Change Speed',cursor="-"):
		self.figure, self.ax = plt.subplots()
		self.figure.suptitle(suptitle, fontsize=20)
		plt.xlabel(xlabel, fontsize=18)
		plt.ylabel(ylabel, fontsize=16)
		self.lines, = self.ax.plot([], [], cursor)
		self.ax.set_autoscaley_on(True)
		self.ax.set_xlim(self.min_x, self.max_x)
		self.ax.grid()

	def addPoint(self,x,y):
		self.xdata.append(x)
		self.ydata.append(y)
		self.lines.set_xdata(self.xdata)
		self.lines.set_ydata(self.ydata)
		
		if(x > self.max_x):
			self.max_x = x * 1.5
		#Need both of these in order to rescale
		self.ax.set_xlim(self.min_x, self.max_x)
		self.ax.relim()
		self.ax.autoscale_view()
		#We need to draw *and* flush
		self.figure.canvas.draw()
		self.figure.canvas.flush_events()