import os
from enum import Enum
from datetime import datetime

# Path to log file
LogFile = '{}//logging.log'.format(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# First log flag
FirstLogging = True
# ----- Log settings -----
UseLogFile = True
# Setting - Log only WARNING and ERROR in file
HighValueLogging = False
# Maximum line numbers in log file
MaxLineNumber = 500
# ------------------------

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
                f.write(f"{datetime.now().strftime('%d.%m.%Y-%H:%M:%S')} SYSTEM> Logfile created - HighValueLogging={HighValueLogging} - UseLogFile={UseLogFile}\n")
            FirstLogging = False
        
        # Skip here if no log file should be used
        if not UseLogFile:
            return

        if not HighValueLogging or (HighValueLogging and (_type == WarningLevel.Warning or _type == WarningLevel.Error)):
            # Add char return
            logText = logText +"\n"
            
            # Read back log file
            lines = []
            with open(LogFile, 'r') as f:
                lines = f.readlines()

            # When max line number has been reached remove oldest entry
            if len(lines) >= MaxLineNumber:
                lines.remove(0)
            lines.append(logText)

            # Write in log file
            with open(LogFile, 'w') as f:
                f.writelines(lines)
    except Exception as e:
        print(f'WARNING> Could not write in log file: {type(e).__name__}, Args: {e.args}')
    

# Log info
def log_info(_msg):
    _logging(WarningLevel.Info, _msg)
# Log warning
def log_warning(_msg):
    _logging(WarningLevel.Warning, _msg)
# Log error
def log_error(_msg):
    _logging(WarningLevel.Error, _msg)