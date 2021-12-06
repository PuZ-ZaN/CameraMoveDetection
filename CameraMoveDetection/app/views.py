
from datetime import datetime
from flask import render_template
from . import app

sensorArr=[]

@app.route("/")
def index():
	return render_template('index.html',sensorTab=sensorArr)

@app.route("/callback")
def callback(data):
	sensorArr.append(data)
	return 'echo!'

@app.route("/sensor")
def callback():
	return render_template('sensor.html',sensorTab=sensorArr) 

@app.route("/add")
def callback():
	return render_template('sensor.html',sensorTab=sensorArr) 

@app.route("/delete<id>")
def callback(id):
	sensorArr.remove(id)
	return 'OK'
