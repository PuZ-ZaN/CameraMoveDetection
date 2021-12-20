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
    CameraId = db.Column(db.Integer, primary_key=True, nullable=False)#autoincrement=True db.Sequence('seq_reg_id', start=1, increment=1)
    Name = db.Column(db.String(50), nullable=False)
    Url = db.Column(db.String(200), nullable=False)
    isMovedBorder = db.Column(db.Integer, nullable=False)
    isMovingBorder = db.Column(db.Integer, nullable=False)

    def __init__(self, Name, Url,isMovedBorder,isMovingBorder):
        self.Name = Name
        self.Url = Url
        self.isMovedBorder = isMovedBorder
        self.isMovingBorder = isMovingBorder

    def __repr__(self):
        return f'{self.CameraId} {self.Name} {self.Url} {self.isMovedBorder} {self.isMovingBorder}'

class Signal(db.Model):
     __tablename__ = 'Signal'
     SignalId = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
     CameraId = db.Column(db.Integer, db.ForeignKey('Camera.CameraId'), nullable=False)
     Image = db.Column(db.Text,nullable=False)
     TimeStamp = db.Column(db.DateTime,nullable=False)
     
     def __init__(self, SignalId, CameraId,isMovedBorder,isMovingBorder):
        self.SignalId = SignalId
        self.CameraId = CameraId
        self.Image = Image
        self.TimeStamp = TimeStamp

     def __repr__(self):
        return f'{self.SignalId} {self.CameraId} {self.Image} {self.TimeStamp}'


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

    def CamerasDelete(name='',source='',isMovingBorder='',isMovedBorder=''):
        db.session.delete(Camera(name,source,isMovingBorder,isMovedBorder))
        db.session.commit()

    def SignalsInsert():
        db.session.add(Signal(name,source,isMovingBorder,isMovedBorder))
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