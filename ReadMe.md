# Overview
The objective of this readme is to spell out all the features the Raspberry Pi module will have, which will include remote control, battery monitoring via a dashboard. 

# Control Panel
The control panel will serve to control different units within the van, which will include the heater and maxair fann. These items need to be controlled so that it they can be triggered automatically from an Alexa command or from the press of a button. Ideally, the control panel is built with Electron so that it can look nice and be launched like an app. 


### Dashboard

1) Time
2) Temperature/Pressure, Humiditiy 
3) Battery Percentage & Remaining Battery & Solar Energy
4) Internet Speed and Wifi Consumption
5) Water Level

### Control Panel

1) Lights (incl. Bathroom Lights, Main Lights, Strobe Lights)
2) Temperature (Heater and MaxxAir Fann) - connection via IR signals
3) Security (Rear and 360 Camera)
4) Water Pump
5) Power (Inverter & 12v) - phone line connection


### Commands

#### SSH into Pi
	ssh pi@192.168.1.33

#### Modify Auto Start Script
	sudo nano /etc/xdg/lxsession/LXDE-pi/autostart

#### How to SSH
	ssh pi@0.tcp.ngrok.io -p10980


tcp://0.tcp.ngrok.io:10980	


### GPIO Pin Configuration


| Name | Relay #  |  Board #     |  GPIO | Color 
|:----------:|:-------------:|:------:|:------:|:------:|
| MaxxAir Fan| 4 | 31 | 6 | Brown|
| Heater| 5 | 29 | 5 | Purple|
| Lights| 6 | 15 | 22 | Green|
| Bathroom | 7 | 13 | 27 | Yellow|
| USB Port| 8 | 11 | 17 | Orange|


### Notes


Black Wire to 8 Module Relay is Ground which connects to Number 6 on the board
Red Wire to 8 Module Relay is 5v wire which connects to Number 4 on the board

Breadboard black can connect to port 14 and breadboard red can connect to number 2

ssh -R 5000:localhost:5000 -i key.pem ec2-user@3.139.104.15 

ssh -R 7070:localhost:22 -i key.pem ec2-user@3.139.104.15 

ssh -R 7070:localhost:22 -i key.pem ec2-user@ec2–3–139–104–15.us-east-2.compute.amazonaws.com


ssh -R localhost:5000:localhost:5000 -i key.pem ec2-user@ec2–3–139–104–15.us-east-2.compute.amazonaws.com

ssh -R 43022:localhost:22 dave@sulaco.local


ssh -i key.pem -R 7070:localhost:22 ec2-user@3.139.104.15 











