import time

from .browser import CBrowser
from selenium.webdriver.common.by import By
from enum import Enum
from datetime import datetime
from lib.settings import  Settings
from lib.logging import log_info, log_warning, log_error

class CFritzBoxBrowser(CBrowser):
    
    # Start browser and open URL
    def open(self):
        webpage = 'http://fritz.box/start'
        log_info(f'Start browser "{webpage}"')
        self.b_start()
        self.b_openPage(link=webpage)

    # Close browser 
    def close(self):
        log_info(f'Close browser')
        self.b_close()

    # Perform login on landing page
    def login(self):
        log_info('Enter password')
        # Enter password
        xpath = '//*[@id="uiPass"]'
        self.b_setTextbox(type=By.XPATH, tag=xpath, text=Settings.Password)
        # Press login button
        xpath = '//*[@id="submitLoginBtn"]'
        self.b_pressButton(type=By.XPATH, tag=xpath)

    # Navigate to online monitor
    def navigate_to_online_monitor(self):
        log_info('Navigate to "Online monitor"')
        # Press Internet
        xpath = '//*[@id="inet"]'
        self.b_pressButton(type=By.XPATH, tag=xpath)
        # Press Online Monitoring
        xpath = '//*[@id="mNetMoni"]'
        self.b_pressButton(type=By.XPATH, tag=xpath)

    def click_tab_online_monitor(self):
        log_info('Click tab "Online monitor"')
        # Press TAB online monitoring
        xpath = '//*[@id="netMoni"]'
        self.b_pressButton(type=By.XPATH, tag=xpath)

    def click_tab_online_zaehler(self):
        log_info('Click tab "Online counter"')
        #Press TAB online counter
        xpath = '//*[@id="netCnt"]'
        self.b_pressButton(type=By.XPATH, tag=xpath)

    # Get current connection data
    def get_connection_data(self):
        log_info('Get connection data...')
        data = dict()
        
        # Get IP4 data
        xpath = '//*[@id="ipv4_info"]/span[1]'
        data['IP4_connect_date'] = datetime.strptime(self.b_getTextValue(type=By.XPATH, tag=xpath), 'verbunden seit %d.%m.%Y, %H:%M Uhr')
        xpath = ' //*[@id="ipv4_info"]/span[2]'
        data['IP4_provider'] = self.b_getTextValue(type=By.XPATH, tag=xpath)
        xpath = '//*[@id="ipv4_info"]/span[3]'
        data['IP4_speed_down'] = float(self.b_getTextValue(type=By.XPATH, tag=xpath).split(' ')[6].replace(',', '.'))
        data['IP4_speed_up'] = float(self.b_getTextValue(type=By.XPATH, tag=xpath).split(' ')[9].replace(',', '.'))
        xpath = '//*[@id="ipv4_info"]/span[4]'
        data['IP4_adress'] = self.b_getTextValue(type=By.XPATH, tag=xpath).split(' ')[1]

        return data
    
    # Get download statistics
    def get_download_data(self):
        log_info('Get download data...')
        data = dict()

        # Get DL data
        xpath = '//*[@id="uiToday"]/td[2]'
        data['DL_online_today'] = int(self.b_getTextValue(type=By.XPATH, tag=xpath).split(':')[0]) * 100 + int(self.b_getTextValue(type=By.XPATH, tag=xpath).split(':')[1])
        xpath = '//*[@id="uiToday"]/td[3]'
        data['DL_datavolume_total'] = int(self.b_getTextValue(type=By.XPATH, tag=xpath))
        xpath = '//*[@id="uiToday"]/td[4]'
        data['DL_datavolume_send'] = int(self.b_getTextValue(type=By.XPATH, tag=xpath))
        xpath = '//*[@id="uiToday"]/td[5]'
        data['DL_datavolume_recive'] = int(self.b_getTextValue(type=By.XPATH, tag=xpath))
        xpath = '//*[@id="uiToday"]/td[6]'
        data['DL_connections'] = int(self.b_getTextValue(type=By.XPATH, tag=xpath))

        return data

    # Click on reconnect button
    def click_reconnect(self):
        log_info('Click "Reconnect" button')
        # Press button
        xpath = '//*[@id="uiReconnectBtn"]'
        self.b_pressButton(type=By.XPATH, tag=xpath)
        log_info('Wait 1 minute...')
        # Wait 1 minute
        time.sleep(60)      

