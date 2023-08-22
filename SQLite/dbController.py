import os, sqlite3
from sqlite3 import Error
from lib.logging import log_info, log_warning, log_error

class CDBConnector:
    DBFile = '{}//database.db'.format(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    # Connection
    Conn = None

    # Execute SQL command
    def execute_SQL(self, com):
        # Create connection if not done
        if self.Conn is None:    
            if self._connect() == -1: 
                return False, -1

        log_info(f"Execute SQL query: {com}")

        suc = True
        try:
            cur = self.Conn.cursor()
            res = cur.execute(com)
            if com.startswith('SELECT'):
                res = res.fetchall()
            if com.startswith('INSERT INTO'):
                self.Conn.commit()
                res = cur.lastrowid
        except Error as e:
            log_error(f"SQL error: {e}")
            suc = False
            res = -1

        return suc, res

    # Private connect
    def _connect(self):
        # Create connection
        try:
            self.Conn = sqlite3.connect(self.DBFile)
        except Error as e:
            log_error(f"Connection to database failed: {e}")
            self._disconnect()
            return -1

        log_info("Connection to database established")
        return 0

    # Private disconnect
    def _disconnect(self):
        # Disconnect
        if self.Conn:
            self.Conn.close()
        self.Conn = None
        log_info("Connection to database has been closed")


class CDBController(CDBConnector):
    
    def __init__(self):
        pass

    def addConnectionData(self, connectData, dlData):
        connectSTR = connectData['IP4_connect_date'].strftime("%d/%m/%Y %H:%M")
        suc, res = self.execute_SQL(f"INSERT INTO CONNECTION(CONNECT_DATE, PROVIDER, SPEED_DOWN, SPEED_UP, ADDRESS) VALUES('{connectSTR}', '{connectData['IP4_provider']}', {connectData['IP4_speed_down']}, {connectData['IP4_speed_up']}, '{connectData['IP4_adress']}')")
        suc, res = self.execute_SQL(f"INSERT INTO DLDATA(CONNECT_DATE, ONLINE, DL_TOTAL, DL_SEND, DL_RECIVE, DL_CONNECTIONS) VALUES('{connectSTR}', {dlData['DL_online_today']}, {dlData['DL_datavolume_total']}, {dlData['DL_datavolume_send']}, {dlData['DL_datavolume_recive']}, {dlData['DL_connections']})")

    # Cleanup database connection
    def close(self):
        self._disconnect()




    