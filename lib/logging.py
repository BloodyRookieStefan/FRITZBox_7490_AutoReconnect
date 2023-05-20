import os
from enum import Enum
from datetime import datetime

# Path to log file
LogFile = '{}//logging.log'.format(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# First log flag
FirstLogging = True
# Setting - Log only WARNING and ERROR in file
HighValueLogging = False

# Enum log level
class WarningLevel(Enum):
    Info = 0
    Warning = 1
    Error = 2

# Private logging function
def _logging(_type, _msg):
    # Access global variable
    global FirstLogging, LogFile
    # Choose prefix
    if _type == WarningLevel.Info:
        preFix = 'INFO>'
    elif _type == WarningLevel.Warning:
        preFix = 'WARNING>'
    elif _type == WarningLevel.Error:
        preFix = 'ERROR>'
    # Build log text
    logText = '{0} {1} {2}'.format(datetime.now().strftime('%d.%m.%Y-%H:%M:%S'), preFix, _msg)
    # Print out log text
    print(logText)
    try:
        # Handle logging file
        if FirstLogging:
            if not os.path.exists(os.path.dirname(LogFile)):
                os.mkdirs(os.path.dirname(LogFile))
            if os.path.exists(LogFile):
                os.remove(LogFile)
            with open(LogFile, 'a') as f:
                f.write(f"{datetime.now().strftime('%d.%m.%Y-%H:%M:%S')} SYSTEM> Logfile created - HighValueLogging=={HighValueLogging}\n")
            FirstLogging = False
        
        if HighValueLogging and (_type == WarningLevel.Warning or _type == WarningLevel.Error) or not HighValueLogging:
            # Write in log file
            with open(LogFile, 'a') as f:
                f.write(logText +"\n")
    except:
        pass
    

# Log info
def log_info(_msg):
    _logging(WarningLevel.Info, _msg)
# Log warning
def log_warning(_msg):
    _logging(WarningLevel.Warning, _msg)
# Log error
def log_error(_msg):
    _logging(WarningLevel.Error, _msg)