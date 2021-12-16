from datetime import datetime
#import json
from flask import render_template, request, Response, jsonify
from CameraApp import app
from . import CameraMoveDetection as CMD
from .db.wrapper import DBApi
from .SmartThreadPool import SmartThreadPool, CPUCountUnavaiableException, MaxThreadsCountReachedException

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

@app.route("/runscript", methods=['POST'])
@app.route("/run", methods=['POST'])
def runscript():
	try:
		request_data = request.get_json()
		print(request_data['name'])
		return ThreadsPool.new_thread(CMD.CalculatePhaseCorrelate, name=request_data['name'], source=request_data['source'], isMovedBorder = int(request_data['isMovedBorder']), isMovingBorder = int(request_data['isMovingBorder']))
	except MaxThreadsCountReachedException as err:
		return str(err)

@app.route("/callback", methods=['POST'])
def callback():
	alarmlist.append(
		{  request.form['name'],
		   request.form['timestamp'],
		   request.form['elapsedSecs'],
		   request.form['IsMoving'],
		   request.form['IsMoved']
		 })
	return ""

@app.route("/getAlarmList", methods=['POST'])
@app.route("/gal", methods=['POST'])
def getAlarmList():
	resp_dict = {'name':alarmlist[0],'timestamp':alarmlist[1],'elapsedSecs':alarmlist[2],'IsMoving':alarmlist[3],'IsMoved':alarmlist[4]}
	return resp_dict


@app.route("/getActiveThreads", methods=['POST'])
@app.route("/gat", methods=['POST'])
def getActiveThreads():
	res = f"alive threads: {ThreadsPool.active_threads_count}\n"
	_counter = 0
	for key in ThreadsPool.threads_list.keys():
		res += f'{_counter}: internal id: {key} - {ThreadsPool.threads_list[key]}\n'
		_counter += 1
	return res 

@app.route('/getThreadsErrors', methods=['POST'])
@app.route('/gte', methods=['POST'])
def getThreadsErrors():
	return ThreadsPool.threads_err

@app.route('/getThreadsPulses', methods=['POST'])
@app.route('/p', methods=['POST'])
def getThreadsPulses():
	return ThreadsPool.threads_pulses