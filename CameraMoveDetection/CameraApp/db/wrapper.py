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

    def __init__(self, Name, Url):
        self.Name = Name
        self.Url = Url

    def __repr__(self):
        return f'{self.CameraId} {self.Name} {self.Url}'

class DBApi():
    def createDb():
        db.create_all()
        db.session.commit()

    def selectAll():
        resultFromDB = Camera.query.all()
        result = []
        for camera in resultFromDB:
            result.append({'Name' : camera.Name, "Url" : camera.Url})
        return result
    
    def insert(name='',source=''):
        db.session.add(Camera(name,source))
        db.session.commit()

    def delete(name='',source=''):
        db.session.delete(Camera(name,source))
        db.session.commit()

#from CameraApp.db.wrapper import db,Camera
#db.create_all()
#db.session.commit()