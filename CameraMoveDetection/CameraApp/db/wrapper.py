from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
#from sqlalchemy.types import Text
from CameraApp import app
#app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://root:root@localhost/CameraMoveDetection?driver=ODBC Driver 17 for SQL Server'
#SQLALCHEMY_TRACK_MODIFICATIONS = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Camera(db.Model):
	__tablename__ = 'Camera'
	CameraId = db.Column(db.Integer, primary_key=True, nullable=False)#autoincrement=True db.Sequence('seq_reg_id', start=1, increment=1)
	Name = db.Column(db.String(50), nullable=False)
	Url = db.Column(db.Text, nullable=False)
	IsMovedBorder = db.Column(db.Integer, nullable=False)
	IsMovingBorder = db.Column(db.Integer, nullable=False)

	def __init__(self,CameraId, Name, Url,isMovedBorder,isMovingBorder):
		self.CameraId = CameraId
		self.Name = Name
		self.Url = Url
		self.isMovedBorder = isMovedBorder
		self.isMovingBorder = isMovingBorder

	def __repr__(self):
		return f'{self.CameraId} {self.Name} {self.Url} {self.isMovedBorder} {self.isMovingBorder}'

class Signal(db.Model):
	__tablename__ = 'Signal'
	CameraId = db.Column(db.Integer, db.ForeignKey('Camera.CameraId'), primary_key=True, nullable=False)
	TimeStamp = db.Column(db.DateTime, primary_key=True, nullable=False)
	Image = db.Column(db.Text,nullable=False)
	IsMoved = db.Column(db.Boolean,server_default="false", nullable=False)
	IsMoving = db.Column(db.Boolean,server_default="false", nullable=False)
	 
	def __init__(self,CameraId,Image,TimeStamp,IsMoved,IsMoving):
		self.CameraId = int(CameraId)
		self.TimeStamp = TimeStamp
		self.Image = Image
		self.IsMoved = bool(IsMoved)
		self.IsMoving = bool(IsMoving)
	def __repr__(self):
		return f'{self.CameraId} {self.TimeStamp} {self.Image} {IsMoved} {IsMoving}'


class DBApi():
	#TODO: есть идея делать несколько последовательных запросов в очередь,
	#коммитить очередь если все норм, иначе делать rollback
	def CamerasSelectAll():
		try:
			resultFromDB = Camera.query.all()
			result = []
			for camera in resultFromDB:
				result.append({
					 "CameraID" : camera.CameraId,
					 "Name" : camera.Name, 
					 "Url" : camera.Url, 
					 "isMovedBorder" : camera.isMovingBorder,
					 "isMovedBorder": camera.isMovedBorder})
			return result
		except IntegrityError as e:
			return "Something wrong with DB"
	
	def CamerasInsert(name='',url='',isMovingBorder='',isMovedBorder=''):
		try:
			db.session.add(Camera(name,url,int(isMovingBorder),int(isMovedBorder)))
			db.session.commit()
		except IntegrityError as e:
			return "Something wrong with DB"
		return "OK"

	def CamerasDelete(cameraID: int):
		try:
			Camera.query.filter(Camera.CameraID == cameraID).delete()
			db.session.commit()
		except IntegrityError as e:
			return "Unknown CameraID or something"
		return "OK"

	def SignalsInsert(cameraId='', timestamp='', image='',isMoved='',isMoving=''):
		try:
			db.session.add(Signal(CameraId=cameraId, TimeStamp=timestamp, Image=image,IsMoved=isMoved,IsMoving=isMoving))
			db.session.commit()
		except IntegrityError as e:
			return "Unknown CameraID, TimeStamp or something"
		return "OK"


	def SignalSelectById(cameraId,timestamp):
		return Signal.query.filter(Signal.CameraId == cameraId, Signal.TimeStamp == timestamp).first()

	def SignalsSelectAll():
		resultFromDB = Signal.query.all()
		result = []
		for signal in resultFromDB:
			result.append({"CameraID" : signal.CameraID, "TimeStamp": signal.TimeStamp, "Image" : signal.Image,"IsMoved": signal.IsMoved,"IsMoving": signal.IsMoving})
		return result

#from CameraApp.db.wrapper import db,Camera
#db.create_all()
#db.session.commit()