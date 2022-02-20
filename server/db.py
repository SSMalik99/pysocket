import string
# import mysql.connector
import pymysql


USER_TABLE_FILLABLE = ["first_name", "last_name", "user_name", "email", "password", "is_logged_in", "created_at", "updated_at"]
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
            self.database = pymysql.connect(
                host = self.host,
                user = self.db_user,
                passwd = self.db_pass,
                cursorclass=pymysql.cursors.DictCursor
            )
        else:
            self.database = pymysql.connect(
                host = self.host,
                user = self.db_user,
                passwd = self.db_pass,
                database= self.db_name,
                cursorclass=pymysql.cursors.DictCursor
            )

        self.cursor = self.database.cursor()

    def closeDb(self):
        self.database.close()
    
    def executeQuery(self):
        self.cursor.execute(self.query)

    def __fetchAllFromCursor(self):
        return self.cursor.fetchall()

    def __fetchOneFromCursor(self):
        return self.cursor.fetchone()
        # return self.cursor.fetchoneDict()
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
            self.query += i.column
            if(index < totalLength):
                self.query += ", "
            index+=1

        self.query +=" );"
        self.executeQuery()

    def inisertData(self, table, data):
        self.query = f"""
        INSERT INTO {table} ( """
        
        if(table=="users"):
            length = 1
            threadLength = USER_TABLE_FILLABLE.__len__()
            for column in USER_TABLE_FILLABLE:
                if(data[column]):
                    self.query += column
                
                if(length < threadLength):
                    self.query += " , "
                
                length+=1
            
            self.query += ") VALUES ("
            
            length = 1
            for column in USER_TABLE_FILLABLE:
                if(data[column]):
                    self.query += f"""'{data[column]}'"""
                
                if(length < threadLength):
                    self.query += " , "
                length+=1
            
            self.query += ") ;"        
        elif(table == "messages"):
            length = 1
            threadLength = MESSAGE_TABLE_FILLABLE.__len__()
            for column in MESSAGE_TABLE_FILLABLE:
                if(data[column]):
                    self.query += column
                
                if(length < threadLength):
                    self.query += " , "
                length+=1

            self.query += ") VALUES ("
            
            length = 1
            for column in MESSAGE_TABLE_FILLABLE:
                if(data[column]):
                    self.query += f"""'{data[column]}'"""
                
                if(length < threadLength):
                    self.query += " , "
                
                length+=1
            self.query += ") ;"
        elif(table == "chat_groups"):
            length = 1
            threadLength = CHAT_GROUP_TABLE_FILLABLE.__len__()
            for column in CHAT_GROUP_TABLE_FILLABLE:
                if(data[column]):
                    self.query += column

                if(length < threadLength):
                    self.query += " , "
                length+=1

            self.query += ") VALUES ("
            
            for column in CHAT_GROUP_TABLE_FILLABLE:
                if(data[column]):
                    self.query += f"""'{data[column]}'"""
                
                if(length < threadLength):
                    self.query += " , "
                length+=1
            
            self.query += ") ;"
        elif(table == "user_groups"):
            length = 1
            threadLength = USER_GROUP_TABLE_FILLABLE.__len__()
            for column in USER_GROUP_TABLE_FILLABLE:
                if(data[column]):
                    self.query += column
                
                if(length < threadLength):
                    self.query += " , "
                
                length+=1
            
            self.query += ") VALUES ("
            
            for column in USER_GROUP_TABLE_FILLABLE:
                if(data[column]):
                    self.query += f"""'{data[column]}'"""
                
                if(length < threadLength):
                    self.query += " , "
                
                length+=1
            
            self.query += ") ;"
        elif(table == "socket_sessions"):
            length = 1
            threadLength = SOCKET_SESSION_TABLE_FILLABLE.__len__()
            for column in SOCKET_SESSION_TABLE_FILLABLE:
                if(data[column]):
                    self.query += column
                
                if(length < threadLength):
                    self.query += " , "
                
                length+=1
            self.query += ") VALUES ("
            
            for column in SOCKET_SESSION_TABLE_FILLABLE:
                if(data[column]):
                    self.query += f"""'{data[column]}'"""
                
                if(length < threadLength):
                    self.query += " , "

                length+=1
            
            self.query += ") ;"
        
        print(self.query)
        self.executeQuery()
        self.commitDb()
    
    def commitDb(self):
        self.database.commit()

    def selectAllFromTable(self, tableName):
        self.query = f"""SELECT * FROM {tableName} ;"""
        self.executeQuery()
        data = self.__fetchAllFromCursor()
        return data
    
    def findFrom(self, table_name):
        self.query = f"""SELECT * FROM {table_name} """
        return DatabaseActions(table_name=table_name)
    
    def findBy(self, table_name, column_name, column_value):
        self.query = f"""SELECT * FROM {table_name} WHERE {column_name} = '{column_value}'"""
        self.executeQuery()
        return self.__fetchOneFromCursor()

    def getFromQuery(self, query, only_one_record = False, return_data = True ):
        self.query = query
        if(return_data):
            self.executeQuery()
            if(only_one_record):
                return self.__fetchOneFromCursor()
            
            return self.__fetchAllFromCursor()
    
    def updateIn(self, table_name) :
        """Initialize a update table instance to alter a table or opdate some values"""
        return UpdateTable(table_name=table_name)
    
    def executeUpdate(self, query):
        self.query = query
        self.executeQuery()

class UpdateTable:
    def __init__(self, table_name) -> None:
        self.table = table_name
        self.alter_query = f"""ALTER TABLE {table_name} """
        self.update_query = f"""UPDATE {table_name} """
    
    def updateColumn(self, column_name, column_value):
        if "SET" not in self.update_query:
            self.update_query += f"""SET {column_name} = '{column_value}' """
        else:
            self.update_query += f""", {column_name} = '{column_value}' """
    
    def updateOn(self, column_name, column_value = False):
        self.update_query += "WHERE "
        if(column_value == False):
            self.update_query += f"""{column_name} = '{column_value}'"""
        else:
            self.update_query += f"""{column_name} <> NULL"""
    
    def getUpdateQuery(self):
        return self.update_query


class DatabaseActions:
    def __init__(self, table_name) -> None:
        self.table_name = table_name
        self.query = f"""SELECT * FROM {self.table_name} """

    def where(self, column_name, column_value):
        if "WHERE" not in self.query:
            self.query += f"""WHERE {column_name} = '{column_value}' """
        else:
            self.query += f""" AND {column_name} = '{column_value}' """
    
    def orWhere(self, column_name, column_value):
        if "WHERE" not in self.query:
            self.query += f"""Where id <> 0 """
        else:
            self.query += f""" or {column_name} = '{column_value}' """
    
    def getQuery(self):
        return self.query

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
        self.column = f"""{self.name} DATETIME """

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