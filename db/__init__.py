import sqlite3
import hashlib

class MainDatabase:
    def __init__(self, db_path = "database/main.db"):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        try:
            self.createTable()
        except:
            print("Table Exists")
    
    def createTable(self):
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        
        self.cursor.execute("""
        self.connection.commit()
            CREATE TABLE users (
                id INTEGER PRIMARY_KEY AUTO_INCREMENT,
                username VARCHAR(16),
                password VARCHAR(64),
                sessionid VARCHAR(244),
                created_on DATETIME,
                usage_count INTEGER DEFAULT 0
            )
        """)
    
    def _insert(self, username: str, password: str, sessionid):
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        print(username, password, sessionid)
        self.cursor.execute(f"INSERT INTO users (username, password, sessionid) VALUES ('{username}', '{password}', '{sessionid}')")
        self.connection.commit()
        
    
    def addUser(self, username, password, sessionid):
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        h_password = hashlib.sha3_256(password.encode("utf-16")).hexdigest()
        self._insert(username, h_password, sessionid)
        return self.getUser(username)[0]
    
    def getUser(self, field: int | str) -> list:
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        
        result = self.cursor.execute(f"SELECT * FROM users WHERE username = '{field}'")
        
        row = result.fetchone()
        if row:
            return row
        
        return []
    
    def loadSession(self, sessionid):
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        
        result = self.cursor.execute(f"SELECT * FROM users WHERE sessionid = '{sessionid}'")
        self.connection.commit()
        rows = result.fetchone()
        if not rows:
            return ""
        else:
            return rows[1]
    
    def saveSession(self, username, sessionid):
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        
        self.cursor.execute(f"UPDATE users SET sessionid = '{sessionid}' WHERE username = '{username}'")
        self.connection.commit()
        return sessionid    
    
    def matchPassword(self, username: str, password)->bool:
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        h_password = hashlib.sha3_256(password.encode("utf-16")).hexdigest()
        pwd = self.getUser(username)[2]
        return pwd == h_password
    
    def usernameTaken(self, username: str) -> bool:
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        
        list = self.getUser(username)
        return len(list) > 0