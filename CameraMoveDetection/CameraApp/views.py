from datetime import datetime
from flask import render_template, request, Response, jsonify
from CameraApp import app
from . import CameraMoveDetection as CMD
from .db.wrapper import DBApi
from .SmartThreadPool import SmartThreadPool, CPUCountUnavaiableException, MaxThreadsCountReachedException
import traceback
import requests

ThreadsPool= SmartThreadPool()
#alarmlist = []

@app.route("/")
def index():
	cameras = DBApi.CamerasSelectAll()
	return render_template('index.html',CameraList=cameras)

@app.route("/addinput", methods=['POST'])
def addInput():
	try:
		#request_data = request.get_json()
		#print(request_data)
		print(request.form)
		DBApi.CamerasInsert(
			name=request.form['name'], 
			source=request.form['source'], 
			isMovedBorder = request.form['isMovedBorder'], 
			isMovingBorder = request.form['isMovingBorder'])
	except Exception as e:
		return traceback.format_exc()
	return "OK"



@app.route("/callback", methods=['POST'])
def callback():
	request_data = request.get_json()
	return DBApi.SignalsInsert(
		cameraId = request_data["CameraID"],
		image = request_data["frame"],
		timestamp = request_data["TimeStamp"],
		isMoving=request_data["IsMoving"],
		isMoved=request_data["IsMoved"]
		)

@app.route("/getAlarmList", methods=['POST'])
@app.route("/gal", methods=['POST'])
def getAlarmList():
	sigs = DBApi.SignalsSelectAll()
	return jsonify(sigs)
	#dict_ret={}
	#for sig in sigs:
	#	dict_ret[sig.SignalId]={
	#		'CameraId' : sig["CameraId"],
	#		'Image': sig["Image"],
	#		'TimeStamp': sig["TimeStamp"],
	#		'IsMoved': sig["IsMoved"],
	#		'IsMoving': sig["IsMoving"]
	#	}
	#return dict_ret


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


@app.route('/getImage', methods=['POST'])
def getImage():
	request_data = request.get_json()
	id = int(request_data['id'])
	return DBApi.SignalSelectById(id)["Image"]

@app.route('/delete', methods=['POST'])
def delete():
	try:
		request_data = request.get_json()
		DBApi.CamerasDelete(request_data ['name'],request_data['source'],request_data['isMovedBorder'],request_data['isMovingBorder'])
	except:
		return "NOT OK"
	return "OK"

@app.route('/edit', methods=['POST'])
def edit():
	try:
		request_data = request.get_json()
		#TODO need optimization
		DBApi.CamerasDelete(
			request_data['oldname'], 
			request_data['oldsource'],
			request_data['oldisMovedBorder'],
			request_data['oldisMovingBorder'])
		DBApi.CamerasInsert(
			request_data['newname'], 
			request_data['newsource'],
			request_data['newisMovedBorder'],
			request_data['newisMovingBorder'])
	except:
		return "NOT OK"
	return "OK"

@app.route("/getCamerasData", methods=['POST'])
def cameraList():
	cameras = DBApi.CamerasSelectAll()
	return jsonify(result=cameras)

@app.route("/runscript", methods=['POST'])
@app.route("/run", methods=['POST'])
def runscript():
	try:
		request_data = request.get_json()
		return ThreadsPool.new_thread(
			CMD.CalculatePhaseCorrelate, 
			CameraID = request_data["CameraID"],
			name=request_data['name'], 
			source=request_data['source'], 
			isMovedBorder = int(request_data['isMovedBorder']), 
			isMovingBorder = int(request_data['isMovingBorder']))
	except MaxThreadsCountReachedException as err:
		return str(err)

@app.route("/runAll", methods=['POST'])
def runAllWorkers():
	cameras = cameraList()
	for cam in cameras:
		requests.post("/run",data={
						'CameraID' : cam["CameraID"],
						'name' : cam["name"],
						'source': cam["source"],
						'isMovedBorder':str(cam["isMovedBorder"]),
						'isMovingBorder':str(cam["isMovingBorder"])
						})
	return cameras


@app.route('/killAll', methods=['POST'])
def killAllWorkers():
	ThreadsPool.abort_all();