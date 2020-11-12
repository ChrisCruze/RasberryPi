#!/usr/bin/python
from flask import Flask, render_template, send_from_directory,redirect,url_for,request
import requests
import os
from flask_restful import Resource, Api,reqparse
from flask_cors import CORS
from supporting_functions import SupportingFunctions,FileFunctions
from multiprocessing import Process
import jobs
import time
import traceback
import json
from sense_hat import SenseHat
import RPi.GPIO as GPIO

server = Flask(__name__)
api = Api(server)
CORS(server)

class MessageHello(Resource):
    def get(self):
        sense = SenseHat()
        sense.show_message("Hello world")

api.add_resource(MessageHello, '/message_hello')

class Pressure(Resource):
    def get(self):
        sense = SenseHat()
        pressure = sense.get_pressure()
        return pressure 

class Temperature(Resource):
    def get(self):
        sense = SenseHat()
        temp = sense.get_temperature()
        return temp 

class Humidity(Resource):
    def get(self):
        sense = SenseHat()
        temp = sense.get_humidity()
        return temp 

class Accelerometer(Resource):
    def get(self):
        sense = SenseHat()
        accelerometer = sense.get_accelerometer_raw()
        return accelerometer 

api.add_resource(Pressure, '/pressure')
api.add_resource(Temperature, '/Temperature')
api.add_resource(Humidity, '/Humidity')
api.add_resource(Accelerometer, '/accelerometer')


class LightOn(Resource):
    def get(self):
        channel = 26
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(channel,GPIO.OUT)
        GPIO.output(channel, GPIO.HIGH)


class LightOff(Resource):
    def get(self):
        channel = 26
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(channel,GPIO.OUT)
        GPIO.output(channel, GPIO.LOW)


api.add_resource(LightOn, '/light_on')
api.add_resource(LightOff, '/light_off')

"""
Below are the API definitions
"""
def read_file(directory):
    with open(directory,'r+') as f:
        r = str(f.read())
    if '.json' in str(directory).lower():
        return json.loads(r)
    else:
        return r

class Read(Resource):
    def get(self,file_id):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        directory = os.path.join(dir_path,'static','jobs')
        directory = os.path.join(directory,file_id)
        return read_file(directory)
api.add_resource(Read, '/read/<string:file_id>')

class Jobs(Resource):
    def get(self):
        directory = FileFunctions().static_directory_get('jobs')
        array = FileFunctions().files_from_directory(directory)
        return array
api.add_resource(Jobs, '/jobs')


class Delete(Resource):
    def get(self,file_id):
        directory = FileFunctions().static_directory_get('jobs')
        file_directory = os.path.join(directory,file_id)
        try:
            os.remove(file_directory)
            return "Successfully Deleted"
        except Exception as err:
            error_message = traceback.format_exc()
            print (error_message)
            return error_message

class Stop(Resource):
    def get(self,file_id):
        directory = FileFunctions().static_directory_get('jobs')
        file_directory = os.path.join(directory,file_id + '.pid')
        try:
            pid = open(file_directory,'r+').read()
            os.kill(pid)
            return "Successfully Stopped"
        except Exception as err:
            error_message = traceback.format_exc()
            print (error_message)
            return error_message


class Start(Resource):
    def get(self,file_id):

        directory = FileFunctions().static_directory_get('jobs')
        file_directory = os.path.join(directory,file_id + '.py')
        try:
            jobs.initiate_python_script(file_directory)
            # script = open(file_directory,'r+').read()
            # f = open(file_directory, 'w+')
            # f.write(script)
        except Exception as err:
            error_message = traceback.format_exc()
            print (error_message)
            jobs.initiate_python_script(file_directory)
            return error_message

api.add_resource(Delete, '/delete/<string:file_id>')
api.add_resource(Stop, '/stop/<string:file_id>')
api.add_resource(Start, '/start/<string:file_id>')



@server.route("/")
def hello():
    return render_template("neomorphism.html")

@server.route("/job")
def script_page(name=None):
    return render_template("job.html")


@server.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        dir_path = os.path.dirname(os.path.realpath(__file__))
        directory = os.path.join(dir_path,'static','jobs',uploaded_file.filename)
        uploaded_file.save(directory)
    return redirect(request.url)



if __name__ == "__main__":
    server.run(host='0.0.0.0', debug=True, threaded=True)

