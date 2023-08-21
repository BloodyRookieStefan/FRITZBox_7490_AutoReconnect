from datetime import datetime
from webController import CWebController
from lib.settings import Settings, OperatingSystem

# ----- Settings ------
Settings.Debug = False                      # Debug mode
Settings.Password = ''                      # Password for login
Settings.System = OperatingSystem.Linux     # Browser type [Linux, Windows]
Settings.DataStorage = True                 # Store data in database
Settings.ReConnectOnStartup = False         # When starting script execute reconnect
Settings.LowResolutionMode = True           # Browser starts with low resulution [<1024x780]
# ---------------------

# Create web controller and join endless loop
webController = CWebController()
webController.loop()