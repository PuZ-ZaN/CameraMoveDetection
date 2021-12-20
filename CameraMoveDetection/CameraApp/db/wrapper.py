from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.types import Text 
from CameraApp import app
#app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://root:root@localhost/CameraMoveDetection?driver=ODBC Driver 17 for SQL Server'
#SQLALCHEMY_TRACK_MODIFICATIONS = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Camera(db.Model):
    __tablename__ = 'Camera'
    CameraId = db.Column(db.Integer, db.Sequence('seq_reg_id', start=1, increment=1), primary_key=True, nullable=False)
    Name = db.Column(db.String(50), nullable=False)
    Url = db.Column(db.String(200), nullable=False)
    isMovedBorder = db.Column(db.Integer, nullable=False)
    isMovingBorder = db.Column(db.Integer, nullable=False)
    def __init__(self, Name, Url,isMovedBorder,isMovingBorder):
        self.Name = Name
        self.Url = Url
        self.isMovedBorder=isMovedBorder
        self.isMovingBorder = isMovingBorder

    def __repr__(self):
        return f'{self.CameraId} {self.Name} {self.Url} {self.isMovedBorder} {self.isMovingBorder}'

class Signals(db.Model):
     __tablename__ = 'Signals'
     SignalId = db.Column(db.Integer, db.Sequence('seq_reg_id', start=1, increment=1), primary_key=True, nullable=False)
     CameraId = db.Column(db.Integer, db.ForeignKey('Camera.CameraId'), nullable=False)
     Image = db.Column(db.Text,nullable=False)
     TimeStamp = db.Column(db.DateTime,nullable=False)


class DBApi():
    def createDb():
        db.create_all()
        db.session.commit()

    def CamerasSelectAll():
        resultFromDB = Camera.query.all()
        result = []
        for camera in resultFromDB:
            result.append({'Name' : camera.Name, 
                           "Url" : camera.Url, 
                           "isMovedBorder" : camera.isMovingBorder,
                           "isMovedBorder": camera.isMovedBorder})
        return result
    
    def CamerasInsert(name='',source='',isMovingBorder='',isMovedBorder=''):
        db.session.add(Camera(name,source,int(isMovingBorder),int(isMovedBorder)))
        db.session.commit()

    def CamerasDelete(name='',source='',isMovingBorder='',isMovedBorder=''):
        db.session.delete(Camera(name,source,isMovingBorder,isMovedBorder))
        db.session.commit()

    def SignalsInsert():
        db.session.add(Camera(name,source,isMovingBorder,isMovedBorder))
        db.session.commit()
    def SignalsDelete():
        db.session.delete(Camera(name,source,isMovingBorder,isMovedBorder))
        db.session.commit()
    def SignalsSelectAll():
        resultFromDB = Signals.query.all()
        result = []
        for signal in resultFromDB:
            result.append({'SignalID' : signal.SignalID, 
                           "CameraID" : signal.CameraID, 
                           "Image" : signal.Image,
                           "TimeStamp": signal.TimeStamp})
        return result

#from CameraApp.db.wrapper import db,Camera
#db.create_all()
#db.session.commit()