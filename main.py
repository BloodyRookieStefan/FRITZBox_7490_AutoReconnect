from datetime import datetime
from webController import CWebController



# Create web controller and join endless loop
webController = CWebController()
webController.loop()