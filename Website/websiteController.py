
from .fritzBoxBrowser import CFritzBoxBrowser

class CWebsiteController():

    # Albatros Browser object
    Browser = None

    def __init__(self) -> None:
        self.Browser = CFritzBoxBrowser()

    # Parse all informations
    def reconnect(self):
        self.Browser.open()                                # Start browser
        self.Browser.login()                               # Login on landing page
        self.Browser.navigate_to_online_monitor()          # Online monitor
        self.Browser.click_tab_online_zaehler()            # Online zaehler
        dlData = self.Browser.get_download_data()          # Get download data     
        self.Browser.click_tab_online_monitor()            # Online monitor        
        connectData = self.Browser.get_connection_data()   # Get connection data since last login
        #self.Browser.click_reconnect()              # Reconnect button
        self.Browser.close()                        # Close browser

        return connectData, dlData