import SQLite
import Website
import time

from datetime import datetime
from lib.settings import CSettings, Settings
from lib.logging import log_info, log_warning, log_error

class CWebController:
    
    LastReconnect = None                    # Datetime of last reconnect
    LastHeartBeat = datetime.now()          # Last heartbeat written in console

    def __init__(self) -> None:
        if Settings.ReConnectOnStartup:
            self.LastReconnect = datetime(1980, 1, 1)
        else:
            self.LastReconnect = datetime.now()

    # Endless loop 
    def loop(self):
        # Validate settings
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
                # Last reconnect is over 1 Hours and current Hour is 3AM
                if ((datetime.now() - self.LastReconnect).total_seconds() > 3601 and datetime.now().hour == 3) or self.LastReconnect.year == 1980:
                    print('Send trigger')
                    self.trigger()
                
                # Send heartbeat
                if datetime.now().hour != self.LastHeartBeat.hour:
                    print(f'Heartbeat at {datetime.now().strftime("%d.%m.%Y-%H")} O\'Clock - Delta: {round((datetime.now() - self.LastReconnect).total_seconds(), 2)}[s] - Last reconnect: {self.LastReconnect.strftime("%d.%m.%Y-%H:%M:%S")}')
                    self.LastHeartBeat = datetime.now()

                self.sleep()

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

    # Sleep till next check
    def sleep(self):
        minToNextHour = 60 - datetime.now().minute
        time.sleep(max((minToNextHour - 2), 1) * 60)    
