from datetime import datetime
#import json
from flask import render_template, request, Response, jsonify
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
	try:
		request_data = request.get_json()
		print(request_data['name'])
		return ThreadsPool.new_thread(CMD.CalculatePhaseCorrelate, name=request_data['name'], source=request_data['source'], isMovedBorder = int(request_data['isMovedBorder']), isMovingBorder = int(request_data['isMovingBorder']))
	except MaxThreadsCountReachedException as err:
		return str(err)

@app.route("/callback", methods=['POST'])
def callback():
	#request_data = request.json
	#print(request.form['name'])
	alarmlist.append(
		{  request.form['name'],
		   request.form['timestamp'],
		   request.form['elapsedSecs'],
		   request.form['IsMoving'],
		   request.form['IsMoved']
		 })
	return ""
	#return request.json['timestamp']#Response(json.dumps(),  mimetype='application/json')

@app.route("/getAlarmList", methods=['POST'])
def getAlarmList():
	res=''
	for i in alarmlist:
		res+=str(i)+r"\n"
	return res#Response(json.dumps(alarmlist),  mimetype='application/json')


@app.route("/getActiveThreads", methods=['POST'])
def getActiveThreads():
	res = f"alive threads: {ThreadsPool.active_threads_count}\n"
	_counter = 0
	for key in ThreadsPool.threads_list.keys():
		res += f'{_counter}: internal id: {key} - {ThreadsPool.threads_list[key]}\n'
		_counter += 1
	return res 

@app.route('/getThreadsErrors', methods=['POST'])
def getThreadsErrors():
	return ThreadsPool.threads_err

@app.route('/getThreadsPulses', methods=['POST'])
def getThreadsPulses():
	return ThreadsPool.threads_pulses