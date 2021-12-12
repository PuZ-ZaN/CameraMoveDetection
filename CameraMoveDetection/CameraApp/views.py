from datetime import datetime
from flask import render_template
from flask import request
from CameraApp import app
from . import CameraMoveDetection as CMD

sensorArr=[]

ThreadsPool=[]
alarmlist = []

@app.route("/")
def index():
	return render_template('index.html',CameraList=[{'name':'rtsp','src':'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4'}])

@app.route("/addinput", methods=['POST'])
def addInput():
	return {request.form['name'] : request.form['source'] }

@app.route("/runscript", methods=['POST'])#Игорь
def runscript():
	#Thread
	#проверка ввреденных данных
	CMD.CalculatePhaseCorrelate(source = request.form['source'],
							 isMovedBorder = request.form['isMovedBorder'],
							 isMovingBorder = request.form['isMovingBorder']
							 )
	#return ok or not ok

@app.route("/callback", methods=['POST'])
def callback():
	pass
	#alarmlist.append({request.name : request.timestamp})