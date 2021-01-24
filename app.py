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
import speedtest  
from gtts import gTTS
from pydub import AudioSegment


server = Flask(__name__)
api = Api(server)
CORS(server)

# class Speak(Resource):
#     def get(self,words):
#         args = request.args
#         audioString = "testing 1 2 3"
#         print(audioString)
#         tts = gTTS(text=audioString, lang='en')
#         tts.save("audio.mp3")
#         sound = AudioSegment.from_mp3("audio.mp3")
#         sound.export("audio.wav", format="wav")
#         os.system("aplay audio.wav")
#         return words

# api.add_resource(Speak, '/speak/<string:words>')

class Speak(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('words')
        parser.add_argument('text', location=['headers','values','json','form'])

        args = parser.parse_args()
        # parsed_json_data = request.json 
        # body_form = request.form 
        audioString = args['words']
        print(audioString)
        tts = gTTS(text=audioString, lang='en')
        tts.save("audio.mp3")
        sound = AudioSegment.from_mp3("audio.mp3")
        sound.export("audio.wav", format="wav")
        os.system("aplay audio.wav")
        #return body_form#,parsed_json_data,request
        try:
            return args
        except Exception as err:
            error_message = traceback.format_exc()
            return error_message



api.add_resource(Speak, '/speak')

class Battery(Resource):
    def get(self):
        # headers = {
        #   'X-Authorization': 'Token 2f183f0829d5b38a01d19d730584b852c6108fd19de9ec0e400e7a66b15ec45f',
        #   'Content-Type': 'text/plain'
        # }
        # url = "https://vrmapi.victronenergy.com/v2/installations/88973/stats"
        url = "https://localhost/signalk/v1/api/"
        #https://192.168.1.33/signalk/v1/api/
        response = requests.request("GET", url,verify=False)
        return response.json()

api.add_resource(Battery, '/battery')






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
api.add_resource(Temperature, '/temperature')
api.add_resource(Humidity, '/humidity')
api.add_resource(Accelerometer, '/accelerometer')


def color_to_rgb(s):
    if s == 'white':
        return (255, 255, 255)
    elif s == 'red':
        return (255,0,0)
    elif s == 'blue':
        return (0,0,255)
    else:
        return (255, 255, 255)

class Color(Resource):
    def get(self,color):
        sense = SenseHat()
        rgb_tup = color_to_rgb(color)
        sense.clear(rgb_tup)

api.add_resource(Color, '/color/<string:color>')



class Sound(Resource):
    def get(self):
        os.system("aplay RaspberryPi/jarvis_intro.wav")
        # os.system("aplay " + num)
        return num

api.add_resource(Sound, '/sound')


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

class On(Resource):
    def get(self,num):
        channel = int(num)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(channel,GPIO.OUT)
        GPIO.output(channel, GPIO.HIGH)

class Off(Resource):
    def get(self,num):
        channel = int(num)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(channel,GPIO.OUT)
        GPIO.output(channel, GPIO.LOW)

api.add_resource(On, '/on/<string:num>')
api.add_resource(Off, '/off/<string:num>')







def bytes_to_megabytes(num):
    try:
        divided_num = num/1000000
        rounded_num = round(divided_num,1)
        return rounded_num
    except:
        return 0 
class DownloadSpeed(Resource):
    def get(self):
        st = speedtest.Speedtest() 
        num = st.download()
        return bytes_to_megabytes(num)

class UploadSpeed(Resource):
    def get(self):
        st = speedtest.Speedtest() 
        num = st.upload()
        return bytes_to_megabytes(num)


api.add_resource(DownloadSpeed, '/download_speed')
api.add_resource(UploadSpeed, '/upload_speed')


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
        directory = os.getcwd()#FileFunctions().static_directory_get('jobs')
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
    server.run(host='0.0.0.0', threaded=True) #, , port=80 debug=True

