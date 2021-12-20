from datetime import datetime
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
	alarmlist.append({
		'name' : request.form['name'],
		'timestamp': request.form['timestamp'],
		'elapsedSecs': request.form['elapsedSecs'],
		'IsMoving': request.form['IsMoving'],
		'IsMoved': request.form['IsMoved'],
		'frame' : request.form['frame']
		})
	return "OK"

@app.route("/getAlarmList", methods=['POST'])
@app.route("/gal", methods=['POST'])
def getAlarmList():
	dict_ret={}
	for i in range(len(alarmlist)):
		dict_ret[i]={
			'name' : alarmlist[i]['name'],
			'timestamp': alarmlist[i]['timestamp'],
			'elapsedSecs': alarmlist[i]['elapsedSecs'],
			'IsMoving': alarmlist[i]['IsMoving'],
			'IsMoved': alarmlist[i]['IsMoved']
		}
	return dict_ret


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
	if len(alarmlist)>id and id>0:
		return alarmlist[id]['frame']
	return "Incorrect id"

@app.route("/addinput", methods=['POST'])
@app.route("/ai", methods=['POST'])
def addInput():
	try:
		DBApi.insert(request.form['name'], request.form['source'],request.form['isMovedBorder'],request.form['isMovingBorder'])
	except:
		return "NOT OK"
	return "OK"

@app.route('/delete', methods=['POST'])
@app.route('/d', methods=['POST'])
def delete():
	request_data = request.get_json()
	name = int(request_data['name'])
	source = int(request_data['source'])
	try:
		DBApi.delete(name,source)
	except:
		return "NOT OK"
	return "OK"

@app.route('/edit', methods=['POST'])
@app.route('/e', methods=['POST'])
def edit():
	oldname = int(request_data['oldname'])
	oldsource = int(request_data['oldsource'])
	newname = int(request_data['newname'])
	newsource = int(request_data['newsource'])
	try:
		DBApi.delete(oldname,oldsource)
		DBApi.insert(newname,newsource)
	except:
		return "NOT OK"
	return "OK"

def init():
	pass

init()