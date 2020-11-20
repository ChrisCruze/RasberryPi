ssh pi@192.168.1.33
zeus

cd RaspberryPi 
python app.py 

cd raspberry-electron
export DISPLAY=:0
npm start

cd
sudo bash startsample.sh
