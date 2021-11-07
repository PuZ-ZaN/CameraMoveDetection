class History:
	hisArray = None
	lenArray = None
	def __init__(self, len = 100):
		super().__init__()
		self.hisArray = []
		self.lenArray = len

	def append(self, lastE : float) -> None:
		if len(self.hisArray) >= self.lenArray:
			self.hisArray.pop(0)
		self.hisArray.append(lastE)

	def avgCalc(self):
		leng = len(self.hisArray)
		if leng > 0:
			return sum(self.hisArray)/leng
		return None

