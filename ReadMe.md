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


### GPIO Pin Configuration
Three Relay Board
Physical 37 - 26 - 
Physical 38 - 20 - 
Physical 40 - 21 - 

Eight Relay Board
K1 - 
K2 - 
K3 - 
K4 - Physical 31 - GPIO 6 - MaxxAir Fan - BLUE
K5 - Physical 29 - GPIO 5 - Diesel Heater - PURPLE
K6 - Physical 15 - GPIO 22 - All the Lights - GREEN
K7 - Physical 13  - GPIO 27 - Bathroom Light - YELLOW
K8 - Physical 11 - GPIO 17 - USB Port - ORANGE















24 - 360 Camera (TBD)
27 - Rear View Camera (TBD)
22 - Inverter (TBD)
23 - Water Pump (TBD)
17 - USB Port (K8)
25 - Bathroom Lights
5 - Main Lights 
6 - 



12v usb
heater 
max air fann
lights
bathroom lights