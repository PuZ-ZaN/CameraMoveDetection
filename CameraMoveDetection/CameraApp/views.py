
from datetime import datetime
from flask import render_template
from CameraApp import app

sensorArr=[]

@app.route("/")
def index():
	return render_template('index.html',sensorTab=sensorArr)

@app.route("/callback")
def callback1(data):
	sensorArr.append(data)
	return 'echo!'

@app.route("/sensor")
def callback2():
	return render_template('sensor.html',sensorTab=sensorArr) 

@app.route("/add")
def callback3():
	return render_template('sensor.html',sensorTab=sensorArr) 

@app.route("/delete<id>")
def callback4(id):
	sensorArr.remove(id)
	return 'OK'
