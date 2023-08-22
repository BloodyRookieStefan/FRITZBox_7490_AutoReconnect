# FRITZBox_7490_AutoReconnect
Reconnect automatically every 24 hours to your DSL provider using 
## Requirements
* Python 3.7 [www.python.org](https://www.python.org/)
* Selenium package
* Chrome webbrowser [www.google.de/chrome](https://www.google.de/chrome/?brand=CHBD&gclid=EAIaIQobChMI_8T96KrM8AIVCm8YCh3TGQYuEAAYASAAEgI32_D_BwE&gclsrc=aw.ds)
## How to install on Raspberry PI 4
* Install Ubuntu Desktop 22.04.2 LTS [www.ubuntu.com](https://ubuntu.com/download/raspberry-pi)
* Get latest updates: `sudo apt update && sudo apt upgrade -y`
* If not installed get Python3 `sudo apt-get install python3`
* Install pip command `sudo apt-get install python3-pip`
* Install Selenium `pip install selenium`
* Install Chrome webbrowser `sudo apt install chromium-browser`
* Install Chromium driver `sudo apt-get install chromium-chromedriver`
## Start python script as service on startup (Option 1)
Create `/etc/systemd/system/myscript.service`
```
[Unit]
Description=My Script

[Service]
ExecStart=/usr/bin/python3 /path/script.py

[Install]
WantedBy=multi-user.target
```
Start service with
```
sudo systemctl start myscript    # Runs the script now
sudo systemctl enable myscript   # Sets the script to run every boot
```
## How to run manually (Option 2)
Execute `main.py`
## Change reconnect time
Open file `./webController.py`  
Change line as desired  
```python
 if ((datetime.now() - self.LastReconnect).total_seconds() > 10800 and datetime.now().hour == 3)
```