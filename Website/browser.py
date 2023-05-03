import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lib.settings import  Settings, OperatingSystem

class CBrowser:

    ChromeDriverPath = '{}//chromedriver.exe'.format(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    Driver = None

    # Start browser
    def b_start(self):
        # Check if EXE exists
        if not os.path.exists(self.ChromeDriverPath):
            raise FileNotFoundError(f'Chromedriver.exe does not exist: {self.ChromeDriverPath}')
        # Browser options
        optionsList = ['--incognito']
        # Create CHROME arguments
        options = webdriver.ChromeOptions()
        for option in optionsList:
            options.add_argument(option)
        # Create CHROME object with options
        if Settings.System == OperatingSystem.Windows:
            # Use this for WINDOWS
            self.Driver = webdriver.Chrome(executable_path=self.ChromeDriverPath, options=options)
        else:
            # Use this for LINUX
            self.Driver = webdriver.Chrome(options=options)
        self.Driver.maximize_window()

    # Close webbrowser
    def b_close(self):
        self.Driver.close()
        self.Driver = None

    # Open any URL
    # link = URL of website
    def b_openPage(self, link):
        self.Driver.get(link)

    # Refresh webpage
    def b_refresh(self):
        self.Driver.refresh()

    # Get text value from attribute
    def b_getTextValue(self, type, tag, to=600):
        # Wait till button is present
        self.b_wait_until_tag_is_present(type=type, tag=tag)
        # Search and get element data
        return self.Driver.find_element(type, tag).text.strip()

    # Wait until tag is loaded
    # type = By.ID / By.CLASS_NAME ....
    # tag = Name of item
    # to = Timeout in seconds
    def b_wait_until_tag_is_present(self, type, tag, to=600):
        WebDriverWait(self.Driver, to).until(EC.presence_of_element_located((type, tag))) 

    # Wait until tag is clickable
    # type = By.ID / By.CLASS_NAME ....
    # tag = Name of item
    # to = Timeout in seconds
    def b_wait_until_tag_is_clickable(self, type, tag, to=600):
        WebDriverWait(self.Driver, to).until(EC.element_to_be_clickable((type, tag))) 

    # Switch back to default frame
    def b_switch_toDefaultFrame(self):
        self.Driver.switch_to.default_content()

    # Press any button on website
    # type = By.ID / By.CLASS_NAME ....
    # tag = Name of item
    def b_pressButton(self, type, tag):
        # Wait till button is present
        self.b_wait_until_tag_is_present(type=type, tag=tag)
        # Wait till button is clickable
        self.b_wait_until_tag_is_clickable(type=type, tag=tag)
        # Search and find button
        self.Driver.find_element(type, tag).click()
        
    # Set text to a textbox
    # type = By.ID / By.CLASS_NAME ....
    # tag = Name of item
    # text = Text to write
    def b_setTextbox(self, type, tag, text):
        # Wait till button is clickable
        self.b_wait_until_tag_is_clickable(type=type, tag=tag)
        # Search and find textbox
        self.Driver.find_element(type, tag).send_keys(text)

    