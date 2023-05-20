
from .fritzBoxBrowser import CFritzBoxBrowser
from lib.settings import Settings
from lib.logging import log_info, log_warning, log_error

class CWebsiteController():

    # Albatros Browser object
    Browser = None

    def __init__(self) -> None:
        self.Browser = CFritzBoxBrowser()

    # Parse all informations
    def reconnect(self):
        tryMaxCounter = 3
        i = 0

        while i < tryMaxCounter:
            try:
                self.Browser.open()                                     # Start browser
                self.Browser.login()                                    # Login on landing page
                self.Browser.navigate_to_online_monitor()               # Online monitor

                dlData = None
                connectData = None
                if Settings.DataStorage:
                    self.Browser.click_tab_online_zaehler()            # Online zaehler
                    dlData = self.Browser.get_download_data()          # Get download data     
                    self.Browser.click_tab_online_monitor()            # Online monitor        
                    connectData = self.Browser.get_connection_data()   # Get connection data since last login

                if not Settings.Debug:
                    self.Browser.click_reconnect()                      # Reconnect button
                self.Browser.close()                                    # Close browser
                i = 3
            except Exception as e:
                log_error(f"Browser reconnect failed: {type(e).__name__}, Args: {e.args}")
                i = i + 1

        return connectData, dlData
    

