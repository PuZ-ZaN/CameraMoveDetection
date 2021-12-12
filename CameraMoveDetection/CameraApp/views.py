from datetime import datetime
from flask import render_template
from flask import request
from CameraApp import app
from . import CameraMoveDetection as CMD
from .db.wrapper import DBApi
from .SmartThreadPool import SmartThreadPool, CPUCountUnavaiableException, MaxThreadsCountReachedException

OK = 'SERVER 200' #Я не уверен в том, что я делаю)
FAILURE_INTERNAL = 'SERVER 500'
FAILURE_PUBLIC = 'SERVER 413 UNABLE TO CREATE SERVER THREAD'

sensorArr=[]

ThreadsPool= SmartThreadPool()
alarmlist = []

@app.route("/")
def index():
	cameras = DBApi.selectAll()
	return render_template('index.html',CameraList=cameras)

@app.route("/addinput", methods=['POST'])
def addInput():
	DBApi.insert(request.form['name'], request.form['source'])
	return {request.form['name'] : request.form['source'] }

@app.route("/runscript", methods=['POST'])#Игорь
def runscript():
	#Thread
	#проверка ввреденных данных
	#CMD.CalculatePhaseCorrelate(source = request.form['source'],
	#						 isMovedBorder = request.form['isMovedBorder'],
	#						 isMovingBorder = request.form['isMovingBorder']
	#						 )
	#return ok or not ok

	try:
		ThreadsPool.new_thread(CMD.CalculatePhaseCorrelate, source=request.form['source'], isMovedBorder = request.form['isMovedBorder'], isMovingBorder = request.form['isMovingBorder'])
		return OK #
	except MaxThreadsCountReachedException:
		return FAILURE_PUBLIC
	except:
		return FAILURE_INTERNAL

@app.route("/callback", methods=['POST'])
def callback():
	pass
	#alarmlist.append({request.name : request.timestamp})