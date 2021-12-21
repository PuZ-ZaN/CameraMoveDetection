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
	Url = db.Column(db.String(200), nullable=False)
	isMovedBorder = db.Column(db.Integer, nullable=False)
	isMovingBorder = db.Column(db.Integer, nullable=False)

	def __init__(self,CameraId, Name, Url,isMovedBorder,isMovingBorder):
		self.Name = Name
		self.CameraId = CameraId
		self.Url = Url
		self.isMovedBorder = isMovedBorder
		self.isMovingBorder = isMovingBorder

	def __repr__(self):
		return f'{self.CameraId} {self.Name} {self.Url} {self.isMovedBorder} {self.isMovingBorder}'

class Signal(db.Model):
	__tablename__ = 'Signal'
	SignalId = db.Column(db.Integer, db.Sequence('seq_reg_id', start=1, increment=1), primary_key=True, nullable=False)
	CameraId = db.Column(db.Integer, db.ForeignKey('Camera.CameraId'), nullable=False)
	Image = db.Column(db.Text,nullable=False)
	TimeStamp = db.Column(db.DateTime,nullable=False)
	IsMoved = db.Column(db.Boolean,server_default="false", nullable=False)
	IsMoving = db.Column(db.Boolean,server_default="false", nullable=False)
	 
	def __init__(self,CameraId,Image,TimeStamp,IsMoved,IsMoving):
		#todo убрать SignalId вообще, его роль будет на Timestamp+CameraID
		self.CameraId = int(CameraId)
		self.Image = Image
		self.TimeStamp = TimeStamp
		self.IsMoved = bool(IsMoved)
		self.IsMoving = bool(IsMoving)
	def __repr__(self):
		return f'{self.SignalId} {self.CameraId} {self.Image} {self.TimeStamp} {IsMoved} {IsMoving}'


class DBApi():
	#NOTE: БД лучше создавать скриптом
	#def createDb():
	#    db.create_all()
	#    db.session.commit()


	#TODO: есть идея делать несколько последовательных запросов в очередь,
	#коммитить очередь если все норм, иначе делать rollback
	def CamerasSelectAll():
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
	
	def CamerasInsert(name='',source='',isMovingBorder='',isMovedBorder=''):
		db.session.add(Camera(name,source,int(isMovingBorder),int(isMovedBorder)))
		db.session.commit()

	def CamerasDelete(CameraID: int):
		#db.session.delete(Camera(name,source,isMovingBorder,isMovedBorder))
		Camera.query.filter(Camera.CameraID == CameraID).delete()
		db.session.commit()

	def SignalsInsert(cameraId='',image='',timestamp='',isMoved='',isMoving=''):
		try:
			db.session.add(Signal(CameraId=cameraId, Image=image,TimeStamp=timestamp,IsMoved=isMoved,IsMoving=isMoving))
			db.session.commit()
		except IntegrityError as e:
			return "Unknown CameraID or something"
		return "OK"


	def SignalSelectById(SignalId):
		return Signal.query.filter(Signal.SignalId == SignalId).first()

	def SignalsSelectAll():
		resultFromDB = Signal.query.all()
		result = []
		for signal in resultFromDB:
			result.append({'SignalID' : signal.SignalID, "CameraID" : signal.CameraID, "Image" : signal.Image,"TimeStamp": signal.TimeStamp,"IsMoved": signal.IsMoved,"IsMoving": signal.IsMoving})
		return result

#from CameraApp.db.wrapper import db,Camera
#db.create_all()
#db.session.commit()