import SQLite
import Website
import time

from datetime import datetime
from lib.logging import log_info, log_warning, log_error

class CWebController:
    
    Debug = True
    LastReconnect = None

    def __init__(self) -> None:
        self.LastReconnect = datetime.now()
        
    def loop(self):
        if not self.Debug:
            log_info('Joining endless loop...')
            while True:
                # Last reconnect is over 12 Hours and current Hour is 4AM
                if (datetime.now() - self.LastReconnect).seconds >= 43200 and datetime.now().hour == 4:
                    self.trigger()
                time.sleep(300)
        else:
            log_info('Debug mode - Single execution...')
            self.trigger()

    def trigger(self):
        log_info('#######################################')
        log_info('Start new reconnect...')
        self.LastReconnect = datetime.now()
        connectData, dlData = self.reconnect()
        log_info('--------------------------------------')
        log_info('Store collected data...')
        self.storeData(connectData, dlData)

    def reconnect(self):
        fritzBox = Website.CWebsiteController()
        return fritzBox.reconnect()
    
    def storeData(self, connectData, dlData):
        sqlController = SQLite.CDBController()
        sqlController.addConnectionData(connectData, dlData)
        sqlController.close()
