import time, re

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
        # If low resulution mode => Click logo first in order to open menue
        if Settings.LowResolutionMode:
            log_info(f'Execute with low resulution mode')
            xpath = '//*[@id="blueBarLogo"]'
            self.b_pressButton(type=By.XPATH, tag=xpath)
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
        xpath = '//*[@id="uiDslIpv4"]/div[3]'
        dataIPv4Raw = self.b_getTextValue(type=By.XPATH, tag=xpath)

        # Connection time
        regexSTR = '^[aA-xX ]+([0-9.]+), ([0-9]+:[0-9]+).*$'
        g = self.regex(regexSTR, dataIPv4Raw)
        data['IP4_connect_date'] = datetime.strptime(f'{g[0]}, {g[1]}', '%d.%m.%Y, %H:%M')
        # Provider
        regexSTR = '^.*, .*, ([aA-zZ]+), .*$'
        g = self.regex(regexSTR, dataIPv4Raw)
        data['IP4_provider'] = g[0]
        # Download speed
        regexSTR = '^.*↓ ([0-9,]+) Mbit\/s.*$'
        g = self.regex(regexSTR, dataIPv4Raw)
        data['IP4_speed_down'] = float(g[0].replace(',', '.'))
        # Upload speed
        regexSTR = '^.*↑ ([0-9,]+) Mbit\/s.*$'
        g = self.regex(regexSTR, dataIPv4Raw)
        data['IP4_speed_up'] = float(g[0].replace(',', '.'))
        # IP Adress
        regexSTR = '^.* ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)$'
        g = self.regex(regexSTR, dataIPv4Raw)
        data['IP4_adress'] = g[0]

        return data
    
    # Get download statistics
    def get_download_data(self):
        log_info('Get download data...')
        data = dict()

        # Get DL data
        xpath = '//*[@id="uiYesterday"]/td[2]'
        data['DL_online_today'] = int(self.b_getTextValue(type=By.XPATH, tag=xpath).split(':')[0]) * 100 + int(self.b_getTextValue(type=By.XPATH, tag=xpath).split(':')[1])
        xpath = '//*[@id="uiYesterday"]/td[3]'
        data['DL_datavolume_total'] = int(self.b_getTextValue(type=By.XPATH, tag=xpath))
        xpath = '//*[@id="uiYesterday"]/td[4]'
        data['DL_datavolume_send'] = int(self.b_getTextValue(type=By.XPATH, tag=xpath))
        xpath = '//*[@id="uiYesterday"]/td[5]'
        data['DL_datavolume_recive'] = int(self.b_getTextValue(type=By.XPATH, tag=xpath))
        xpath = '//*[@id="uiYesterday"]/td[6]'
        data['DL_connections'] = int(self.b_getTextValue(type=By.XPATH, tag=xpath))

        return data

    # Click on reconnect button
    def click_reconnect(self):
        log_info('Click "Reconnect" button')
        xpath = '//*[@id="uiReconnectBtn"]'
        self.b_scrollIntoView(type=By.XPATH, tag=xpath)
        # Press button
        self.b_pressButton(type=By.XPATH, tag=xpath)
        log_info('Wait 1 minute...')
        # Wait 1 minute
        time.sleep(60)      

    # Process regex
    def regex(self, pattern, input):
        matches = re.finditer(pattern, input, re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            return match.groups()
