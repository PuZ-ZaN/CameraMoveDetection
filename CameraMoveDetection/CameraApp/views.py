from datetime import datetime
from flask import render_template, request, Response, jsonify
from CameraApp import app
from . import CameraMoveDetection as CMD
from .db.wrapper import DBApi
from .SmartThreadPool import SmartThreadPool, CPUCountUnavaiableException, MaxThreadsCountReachedException
import traceback
import requests

ThreadsPool= SmartThreadPool()
workingThreadUrls = []
threadsErrorList=[]

@app.route("/")
def index():
	cameras = DBApi.CamerasSelectAll()
	return ""#render_template('index.html',CameraList=list(cameras))


#=======CAMERAS CRUD============
@app.route("/CameraAdd", methods=['POST'])
def addInput():
	try:
		if len(request.form)>0:
			request_data = request.form
		else:
			request_data = request.get_json()
			if len(request_data)==0:
				return "KeyError"
		DBApi.CamerasInsert(
			name=request_data['Name'], 
			url=request_data['Url'],
			isMovingBorder = request_data['IsMovingBorder'],
			isMovedBorder = request_data['IsMovedBorder']
			)
	except Exception as e:
		return traceback.format_exc()
	return "OK"

@app.route('/CameraDeleteById', methods=['POST'])
def CameraDeleteById():
	try:
		request_data = request.get_json()
		print(bool(request_data['Hard']))
		res = DBApi.CamerasDelete(DBApi,request_data['Id'],bool(request_data['Hard']))
	except Exception as e:
		return f"NOT OK {e}"
	return res

@app.route('/CameraEdit', methods=['POST'])
def edit():
	try:
		request_data = request.get_json()
		#TODO need optimization
		DBApi.CamerasDelete(
			request_data['oldName'], 
			request_data['oldUrl'],
			request_data['oldIsMovedBorder'],
			request_data['oldIsMovingBorder'])
		DBApi.CamerasInsert(
			request_data['newName'], 
			request_data['newUrl'],
			request_data['newIsMovedBorder'],
			request_data['newIsMovingBorder'])
	except:
		return "NOT OK"
	return "OK"

@app.route("/Cameras", methods=['POST'])
def cameraList():
	cameras = DBApi.CamerasSelectAll()
	return jsonify(cameras)

#=======SIGNALS CRUD============
@app.route("/SignalAdd", methods=['POST'])
def AddNewSignal():
	if request.form is None:
		request_data = request.form
	else:
		request_data = request.get_json()
		if request_data is None:
			return "KeyError"
	return DBApi.SignalsInsert(
		cameraId = request_data["CameraID"],
		image = request_data["Frame"],
		timestamp = request_data["TimeStamp"],
		isMoving=request_data["IsMoving"],
		isMoved=request_data["IsMoved"]
		)

@app.route("/Signals", methods=['POST'])
def SignalsGet():
	sigs = DBApi.SignalsSelectAll()
	print(sigs)
	return jsonify(sigs)

@app.route('/SignalGetImageByIdAndTimestamp', methods=['POST'])
def GetSignalImage():
	try:
		request_data = request.get_json()
		id = int(request_data['Id'])
		ts = request_data['TimeStamp']
		res = DBApi.SignalSelectById(id,ts).Image
		if(res is None):
			return "Nothing"
		return {"Url":res}
	except KeyError:
		return "Unknows Id!"
	except Exception as e:
		return f"Something Wrong! {e}"

#=======THREADS INFO============
@app.route("/Threads", methods=['POST'])
def ThreadsGetActive():
	res = [{
		"Active threads":f"{ThreadsPool.active_threads_count}",
		"Errors": ThreadsPool.threads_err, 
		"Pulses":ThreadsPool.threads_pulses}]
	_counter = 0
	for key in ThreadsPool.threads_list.keys():
		res.append({ key : f"internal id: {key} {ThreadsPool.threads_list[key]}" })
		_counter += 1
	return {"res":res,"Errors":threadsErrorList}

@app.route("/ThreadsErrorHandler", methods=['POST'])
def ThreadsErrorHandler():
	if request.form is None:
		request_data = request.form
	else:
		request_data = request.get_json()
		if request_data is None:
			return "KeyError"
	threadsErrorList.append(request_data["ErrorText"])

#=======THREADS CONTROL============
@app.route("/ThreadRun", methods=['POST'])
def runscript():
	try:
		request_data = request.get_json()
		return ThreadsPool.new_thread(
			CMD.CalculatePhaseCorrelate, 
			CameraID = request_data["CameraID"],
			Url=request_data['Url'], 
			IsMovedBorder = int(request_data['IsMovedBorder']), 
			IsMovingBorder = int(request_data['IsMovingBorder']))
	except MaxThreadsCountReachedException as err:
		return str(err)

@app.route("/ThreadsRunAll", methods=['POST'])
def runAllWorkers():
	cameras = DBApi.CamerasSelectAll()
	for cam in cameras:
		if not cam["Url"] in workingThreadUrls:
			ThreadsPool.new_thread(CMD.CalculatePhaseCorrelate,
				CameraID = cam["CameraId"], 
				Url=cam["Url"], 
				IsMovedBorder = int(cam["IsMovedBorder"]), 
				IsMovingBorder = int(cam["IsMovingBorder"]))

			workingThreadUrls.append(cam["Url"])
	return "OK"
