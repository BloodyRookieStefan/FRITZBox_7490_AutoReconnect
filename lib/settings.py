
from enum import Enum

class OperatingSystem(Enum):
    Linux = 0
    Windows = 1

class CSettings:
    Debug = None
    Password = None
    System = None
    DataStorage = None
    ReConnectOnStartup = None
    LowResolutionMode = None

    def __init__(self) -> None:
        pass

    def validate(self):
        if not isinstance(self.Debug, bool):
            raise ValueError('Invalid data type for Settings.Debug')
        if not isinstance(self.Password, str):
            raise ValueError('Invalid data type for Settings.Password')
        if not isinstance(self.System, OperatingSystem):
            raise ValueError('Invalid data type for Settings.System')
        if not isinstance(self.DataStorage, bool):
            raise ValueError('Invalid data type for Settings.DataStorage')
        if not isinstance(self.ReConnectOnStartup, bool):
            raise ValueError('Invalid data type for Settings.ReConnectOnStartup')
        if not isinstance(self.LowResolutionMode, bool):
            raise ValueError('Invalid data type for Settings.LowResolutionMode')
        
Settings = CSettings()