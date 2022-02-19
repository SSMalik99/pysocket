import string
import mysql.connector


USER_TABLE_FILLABLE = ["first_name", "last_name", "user_name", "email", "password", "created_at", "updated_at"]
MESSAGE_TABLE_FILLABLE = ["message", "is_seen", "sender_id", "reciever_id", 'group_id',"is_group_message", "created_at", "updated_at"]
CHAT_GROUP_TABLE_FILLABLE = ['name', 'admin_id', 'is_private', "created_at", "updated_at"]
USER_GROUP_TABLE_FILLABLE = ['user_id', "group_id", "created_at", "updated_at"]
SOCKET_SESSION_TABLE_FILLABLE = ['user_id', "session_id", "created_at", "updated_at"]

class Database:
    def __init__(self, db_host="127.0.0.1", db_user="root", db_pass="root") -> None:
        self.host = db_host
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_name = False

    def connectDb(self):
        if self.db_name == False:
            self.database = mysql.connector.connect(
                host = self.host,
                user = self.db_user,
                passwd = self.db_pass
            )
        else:
            self.database = mysql.connector.connect(
                host = self.host,
                user = self.db_user,
                passwd = self.db_pass,
                database= self.db_name
            )

        self.cursor = self.database.cursor()

    def closeDb(self):
        self.database.close()
    
    def executeQuery(self):
        self.cursor.execute(self.query)

    def createDatabase(self, db_name):
        self.query = f"""CREATE DATABASE IF NOT EXISTS {db_name}"""
        self.db_name = db_name
        self.executeQuery()
        self.closeDb()
        self.connectDb()

    
    def createTable(self, table_name):
        self.table = f"""CREATE TABLE IF NOT EXISTS {table_name} """
        # self.executeQuery()
    def makeMyTable(self, *coulmns):
        self.query = self.table+" ( "
        totalLength = coulmns.__len__()
        index = 1
        for i in coulmns:
            self.query += i
            if(index < totalLength):
                self.query += ", "
            index+=1

        self.query +=" );"
        print(self.query)
        self.executeQuery()

    def inisertData(self, table, data):
        self.query = f"""
        INSERT INTO {table} ( """
        
        if(table=="users"):
            length = 1
            threadLength = USER_TABLE_FILLABLE.__len__()
            for column in USER_TABLE_FILLABLE:
                if(data.column):
                    self.query += column
                
                if(length < threadLength):
                    self.query += " , "
            
            self.query += ") VALUES ("
            
            for column in USER_TABLE_FILLABLE:
                if(data.column):
                    self.query += data.column
                
                if(length < threadLength):
                    self.query += " , "
            
            self.query += ") ;"        
        elif(table == "messages"):
            length = 1
            threadLength = MESSAGE_TABLE_FILLABLE.__len__()
            for column in MESSAGE_TABLE_FILLABLE:
                if(data.column):
                    self.query += column
                
                if(length < threadLength):
                    self.query += " , "
            
            self.query += ") VALUES ("
            
            for column in MESSAGE_TABLE_FILLABLE:
                if(data.column):
                    self.query += data.column
                
                if(length < threadLength):
                    self.query += " , "
            
            self.query += ") ;"
        elif(table == "chat_groups"):
            length = 1
            threadLength = CHAT_GROUP_TABLE_FILLABLE.__len__()
            for column in CHAT_GROUP_TABLE_FILLABLE:
                if(data.column):
                    self.query += column
                
                if(length < threadLength):
                    self.query += " , "
            
            self.query += ") VALUES ("
            
            for column in CHAT_GROUP_TABLE_FILLABLE:
                if(data.column):
                    self.query += data.column
                
                if(length < threadLength):
                    self.query += " , "
            
            self.query += ") ;"
        elif(table == "user_groups"):
            length = 1
            threadLength = USER_GROUP_TABLE_FILLABLE.__len__()
            for column in USER_GROUP_TABLE_FILLABLE:
                if(data.column):
                    self.query += column
                
                if(length < threadLength):
                    self.query += " , "
            
            self.query += ") VALUES ("
            
            for column in USER_GROUP_TABLE_FILLABLE:
                if(data.column):
                    self.query += data.column
                
                if(length < threadLength):
                    self.query += " , "
            
            self.query += ") ;"
        elif(table == "socket_sessions"):
            length = 1
            threadLength = SOCKET_SESSION_TABLE_FILLABLE.__len__()
            for column in SOCKET_SESSION_TABLE_FILLABLE:
                if(data.column):
                    self.query += column
                
                if(length < threadLength):
                    self.query += " , "
            
            self.query += ") VALUES ("
            
            for column in SOCKET_SESSION_TABLE_FILLABLE:
                if(data.column):
                    self.query += data.column
                
                if(length < threadLength):
                    self.query += " , "
            
            self.query += ") ;"
            
        self.executeQuery()
class TableColumn:
    def __init__(self, name) -> None:
        self.name = name
    # Column creation method add whatever you want to add
    def string_column(self, length=255):
        self.column =  f"""{self.name} VARCHAR({length}) """
    
    def int_columm(self,  auto_increment=False):
        if(auto_increment):
            self.column = f"""{self.name} INT AUTO_INCREMENT """
        
        self.column = f"""{self.name} INT """
    def big_int(self, auto_increment = True):
        if(auto_increment):
            self.column = f"""{self.name} BIGINT AUTO_INCREMENT """
        else:
            self.column = f"""{self.name} INT """
    def text_column(self):
        self.column = f"""{self.name} TEXT """

    def bool_column(self):
        self.column = f"""{self.name} BOOLEAN """

    def date_time_column(self):
        self.column = f"""{self.name} DATETIME"""

    # add index methodss
    def uniqueIndex(self):
        self.column += "UNIQUE "
    def primaryIndex(self):
        self.column += f"""PRIMARY KEY """

    def nullAble(self, nullAble=True):
        
        if(nullAble):
            self.column += "NULL "
        else:
            self.column += "NOT NULL "

    def defaultValue(self, value):
        self.column += f"""DEFAULT {value} """
    # create coulmn
    def createColumn(self) -> string:
        return self.column
        # self.executeQuery()

# print(sum, int(sum/2))