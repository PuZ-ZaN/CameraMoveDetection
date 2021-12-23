from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_, not_,text
from sqlalchemy.exc import IntegrityError
import json
#from sqlalchemy.types import Text
from CameraApp import app
from datetime import datetime
#app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://root:root@localhost/CameraMoveDetection?driver=ODBC Driver 17 for SQL Server'
#SQLALCHEMY_TRACK_MODIFICATIONS = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from sqlalchemy.inspection import inspect

class Serializer(object):

	def serialize(self):
		return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

	@staticmethod
	def serialize_list(l):
		return [m.serialize() for m in l]

class Camera(db.Model):
	__tablename__ = 'Camera'
	CameraId = db.Column(db.Integer, primary_key=True, nullable=False)#autoincrement=True db.Sequence('seq_reg_id', start=1, increment=1)
	Name = db.Column(db.String(50), nullable=False)
	Url = db.Column(db.Text, nullable=False)
	IsMovedBorder = db.Column(db.Integer, nullable=False)
	IsMovingBorder = db.Column(db.Integer, nullable=False)

	#def __init__(self, Name='', Url='',isMovedBorder='100',isMovingBorder='100'):
	#	self.CameraId = CameraId
	#	self.Name = Name
	#	self.Url = Url
	#	self.IsMovedBorder = int(isMovedBorder)
	#	self.IsMovingBorder = int(isMovingBorder)

	def __repr__(self):
		return f'{self.CameraId} {self.Name} {self.Url} {self.isMovedBorder} {self.isMovingBorder}'

	def dict(self):
		return {
			"CameraId":self.CameraId,
			"Name":self.Name,
			"Url":self.Url ,
			"IsMovedBorder":self.IsMovedBorder ,
			"IsMovingBorder":self.IsMovingBorder
		  }


class Signal(db.Model):
	__tablename__ = 'Signal'
	CameraId = db.Column(db.Integer, db.ForeignKey('Camera.CameraId'), primary_key=True, nullable=False)
	TimeStamp = db.Column(db.DateTime, primary_key=True, nullable=False)
	Image = db.Column(db.Text,nullable=False)
	IsMoved = db.Column(db.Boolean,server_default="false", nullable=False)
	IsMoving = db.Column(db.Boolean,server_default="false", nullable=False)
	 
	#def __init__(self,CameraId,Image,TimeStamp,IsMoved,IsMoving):
	#	self.CameraId = int(CameraId)
	#	self.TimeStamp = TimeStamp
	#	self.Image = Image
	#	self.IsMoved = bool(IsMoved)
	#	self.IsMoving = bool(IsMoving)

	def __repr__(self):
		return f'{self.CameraId} {self.TimeStamp} {self.Image} {IsMoved} {IsMoving}'

	def dict(self):
		return {
		  "CameraId":self.CameraId,
		  "TimeStamp":self.TimeStamp,
		  "Image":self.Image,
		  "IsMoved":self.IsMoved,
		  "IsMoving":self.IsMoving
		  }


class DBApi():
	#TODO: есть идея делать несколько последовательных запросов в очередь,
	#коммитить очередь если все норм, иначе делать rollback
	def CamerasSelectAll():
		try:
			resultFromDB = Camera.query.all()
			ls = []
			for i in resultFromDB:
				ls.append(i.dict())
			return ls
		except IntegrityError as e:
			return "Something wrong with DB"

	def SignalsSelectAll():
		try:
			resultFromDB = Signal.query.all()
			ls = []
			for i in resultFromDB:
				ls.append(i.dict())
			return ls
		except IntegrityError as e:
				return "Something wrong with DB"








	def SignalsGetSpecific(CameraID,TimeStamp):
		try:#Signal.CameraID==CameraID and 
			resultFromDB = db.session.query(Signal).filter(Signal.TimeStamp==(TimeStamp),Signal.CameraId==(CameraID))
			#Signal.query.filter(int(CameraID))
			#query = db.session.query(Signal).filter(User.CameraID.like(int(CameraID)),User.TimeStamp.like(TimeStamp))
			#db.session.query(Signal).filter(Signal.TimeStamp==TimeStamp|Signal.CameraID==CameraID).all()
			#Signal.query.filter(Signal.TimeStamp==TimeStamp).all()
			lsa = []
			for i in resultFromDB:
				lsa.append(i.dict())   #.latest(datetime.strptime(TimeStamp, "%d-%m-%Y %H:%M:%S")))
			return lsa
		except IntegrityError as e:
				return "Something wrong with DB"
	











	def CamerasInsert(name='',url='',isMovingBorder='',isMovedBorder=''):
		try:
			db.session.add(Camera(
				Name = name,
				Url = url,
				IsMovedBorder = int(isMovingBorder),
				IsMovingBorder = int(isMovedBorder)))
			db.session.commit()
		except IntegrityError as e:
			return "Something wrong with DB"
		return "OK"

	def SignalsInsert(cameraId='', timestamp='', image='',isMoved='',isMoving=''):
		try:
			db.session.add(Signal(
				CameraId=int(cameraId), 
				TimeStamp=datetime.strptime(timestamp, "%d/%m/%Y %H:%M:%S"), 
				Image=image,
				IsMoved=bool(isMoved),
				IsMoving=bool(isMoving)))
			db.session.commit()
		except IntegrityError as e:
			return f"Unknown CameraID or TimeStamp already in base"
		return "OK"

	def SignalsDeleteByCameraId(cameraId):
		try:
			Signal.query.filter(Signal.CameraId == cameraId).delete()
		except IntegrityError as e:
			return f"Unknown CameraID or have undeleted signals"
		return "OK"
	def CamerasDelete(self,cameraID,hard):
		try:
			if(hard==True):
				self.SignalsDeleteByCameraId(cameraID)
				db.session.commit()
			Camera.query.filter(Camera.CameraId == int(cameraID)).delete()
			db.session.commit()
		except IntegrityError as e:
			return f"Unknown CameraID or have undeleted signals {e}"
		return "OK"




	def SignalSelectById(cameraId,TimeStamp):
		return Signal.query.filter(Signal.CameraId == cameraId, Signal.TimeStamp == TimeStamp).first()



#from CameraApp.db.wrapper import db,Camera
#db.create_all()
#db.session.commit()