from datetime import datetime
from webController import CWebController
from lib.settings import Settings, OperatingSystem

# ----- Settings ------
Settings.Debug = False
Settings.Password = ''
Settings.System = OperatingSystem.Linux
Settings.DataStorage = True
# ---------------------

# Create web controller and join endless loop
webController = CWebController()
webController.loop()