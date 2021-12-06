
from datetime import datetime
from flask import render_template
from CameraApp import app

sensorArr=[]

@app.route("/")
def index():
	return render_template('index.html',CameraList=[{'name':'rtsp','src':'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4'}])

@app.route("/addinput", methods=['POST'])
def addInput():
	name = request.form['name']
	return name
