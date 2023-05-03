import SQLite
import Website
import time

from datetime import datetime
from lib.settings import CSettings, Settings
from lib.logging import log_info, log_warning, log_error

class CWebController:
    
    Debug = False               # Debug flag
    LastReconnect = None        # Datetime of last reconnect

    def __init__(self) -> None:
        self.LastReconnect = datetime.now()

    # Endless loop 
    def loop(self):

        if isinstance(Settings, CSettings):
            Settings.validate()
        else:
            raise ValueError('Invalid data type for settings')
        
        if Settings.Debug:
            log_info('Debug mode - Single execution...')
            self.trigger()
        else:
            log_info('Joining endless loop...')
            while True:
                # Last reconnect is over 3 Hours and current Hour is 3AM
                if (datetime.now() - self.LastReconnect).seconds > 10800 and datetime.now().hour == 3:
                    self.trigger()
                # Wait 1 minutes
                time.sleep(60)

    # Trigger for reconnect
    def trigger(self):
        log_info('#######################################')
        log_info('Start reconnect...')
        self.LastReconnect = datetime.now()
        connectData, dlData = self.reconnect()
        log_info('--------------------------------------')
        if Settings.DataStorage:
            log_info('Store collected data...')
            self.storeData(connectData, dlData)
        log_info('Done')
        log_info('Wait for new trigger...')

    # Reconnect on browser
    def reconnect(self):
        fritzBox = Website.CWebsiteController()
        return fritzBox.reconnect()
    
    # Store data in SQL
    def storeData(self, connectData, dlData):
        if connectData is None:
            log_warning('Connect data is empty... Skip data storage')
            return
        if dlData is None:
            log_warning('Download data is empty... Skip data storage')
            return
        # Create SQL controller
        sqlController = SQLite.CDBController()
        sqlController.addConnectionData(connectData, dlData)
        sqlController.close()
