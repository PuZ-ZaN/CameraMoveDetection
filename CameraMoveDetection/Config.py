class Config:
	isMovedBorder = 100
	isMovingBorder = 100
	etalonChangeEveryNFps = 500
	filename = "datasets/g.mp4"
	NameVideoWindow = "Frame"
	ShowVideo = True
	etalonHistoryLen=50
	staticHistoryLen=70
	def __init__(self,configPath="./config.xml"):
		import xml.etree.ElementTree as ET
		root = ET.parse(configPath).getroot()
		configAsDict={each.tag:each.text for each in root}

		self.isMovedBorder = int(configAsDict['isMovedBorder'])
		self.isMovingBorder = int(configAsDict['isMovingBorder'])
		self.etalonChangeEveryNFps = int(configAsDict['etalonChangeEveryNFps'])
		self.filename = configAsDict['filename']
		self.NameVideoWindow = configAsDict['NameVideoWindow']
		self.ShowVideo = bool(configAsDict['ShowVideo'])
		self.staticHistoryLen = int(configAsDict['etalonHistoryLen'])
		self.etalonHistoryLen = int(configAsDict['staticHistoryLen'])
		