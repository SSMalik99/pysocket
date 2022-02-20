from datetime import datetime
import eventlet
import string
import random
from matplotlib import table
import socketio
import db

dbHost= "127.0.0.1"
dbUser = "root"
dbPassword = "bubby"
dbName = "chat_buddy"

database = db.Database(db_host=dbHost, db_user=dbUser, db_pass=dbPassword)
database.connectDb()
database.createDatabase(db_name=dbName)

def createUserTable(tableName="users"):
    
    # Initiallize table
    database.createTable(table_name=tableName)
    
    # Initialize columns
    id = db.TableColumn("id")
    firstName = db.TableColumn("first_name")
    lastName = db.TableColumn("last_name")
    email = db.TableColumn('email')
    password = db.TableColumn('password')
    userName = db.TableColumn('user_name')
    isLoggedIn = db.TableColumn('is_logged_in')
    createdAt = db.TableColumn('created_at')
    updateAt = db.TableColumn('updated_at')

    # define properties for columns
    id.big_int()
    id.primaryIndex()
    id.nullAble(False)
    
    firstName.string_column()
    
    lastName.string_column()
    lastName.nullAble()

    email.string_column()
    email.uniqueIndex()

    password.text_column()
    password.nullAble(False)

    userName.string_column()
    userName.uniqueIndex()

    isLoggedIn.bool_column()
    isLoggedIn.nullAble()
    isLoggedIn.defaultValue(0)

    createdAt.date_time_column()
    createdAt.nullAble()

    updateAt.date_time_column()
    updateAt.nullAble()
    
    # Make table
    database.makeMyTable(id, firstName, lastName, email, password, userName, isLoggedIn, createdAt, updateAt)

def createMessageTable(table_name="messages"):
    # Initiallize table
    database.createTable(table_name=table_name)

    # Initialize columns
    id = db.TableColumn("id")
    message = db.TableColumn("message")
    isSeen = db.TableColumn("is_seen")
    senderId = db.TableColumn('sender_id')
    reciever_id = db.TableColumn('reciever_id')
    groupId = db.TableColumn('group_id')
    isGroupMessage = db.TableColumn('is_group_message')
    createdAt = db.TableColumn('created_at')
    updateAt = db.TableColumn('updated_at')

    # define properties for columns
    id.big_int()
    id.nullAble(False)
    id.primaryIndex()

    message.text_column()
    message.nullAble(False)
    
    isSeen.bool_column()
    isSeen.nullAble()
    isSeen.defaultValue(0)

    senderId.big_int(False)
    
    reciever_id.big_int(False)
    reciever_id.nullAble()

    groupId.big_int(False)
    groupId.nullAble()

    isGroupMessage.bool_column()
    isGroupMessage.nullAble()
    isGroupMessage.defaultValue(0)
    
    createdAt.date_time_column()
    createdAt.nullAble()

    updateAt.date_time_column()
    updateAt.nullAble()

    database.makeMyTable(id, message, isSeen, senderId, reciever_id, groupId, isGroupMessage, createdAt, updateAt)

def createGroupTable(table_name="chat_groups"):
    database.createTable(table_name=table_name)
    # Initialize columns
    id = db.TableColumn("id")
    groupName = db.TableColumn('name')
    adminId = db.TableColumn('admin_id')
    isPrivate = db.TableColumn('is_private')
    createdAt = db.TableColumn('created_at')
    updateAt = db.TableColumn('updated_at')

    # define properties for columns
    id.big_int()
    id.primaryIndex()
    id.nullAble(False)

    groupName.string_column()
    
    adminId.big_int(False)
    
    isPrivate.bool_column()
    isPrivate.nullAble()
    isPrivate.defaultValue(0)

    createdAt.date_time_column()
    createdAt.nullAble()

    updateAt.date_time_column()
    updateAt.nullAble()

    database.makeMyTable(id, groupName, adminId, isPrivate, createdAt, updateAt)

def createUserGroupTable(table_name="user_groups"):
    
    database.createTable(table_name=table_name)

    # Initialize columns
    id = db.TableColumn("id")
    groupId = db.TableColumn('group_id')
    userId = db.TableColumn('user_id')
    createdAt = db.TableColumn('created_at')
    updateAt = db.TableColumn('updated_at')

    # define properties for columns
    id.big_int()
    id.primaryIndex()
    id.nullAble(False)
    
    groupId.big_int(False)
    userId.big_int(False)

    createdAt.date_time_column()
    createdAt.nullAble()

    updateAt.date_time_column()
    updateAt.nullAble()

    database.makeMyTable(id, groupId, userId, createdAt, updateAt)

def createSocketSessionTable(table_name="socket_sessions"):
    database.createTable(table_name=table_name)

    # Initialize columns
    id = db.TableColumn("id")
    socketId = db.TableColumn('socket_id')
    userId = db.TableColumn('user_id')
    createdAt = db.TableColumn('created_at')
    updateAt = db.TableColumn('updated_at')

    # define properties for columns
    id.big_int()
    id.primaryIndex()
    id.nullAble(False)
    
    socketId.big_int(False)
    userId.big_int(False)

    createdAt.date_time_column()
    createdAt.nullAble()

    updateAt.date_time_column()
    updateAt.nullAble()

    database.makeMyTable(id, socketId, userId, createdAt, updateAt)

def createDatabaseTables():
    createUserTable()
    createMessageTable()
    createGroupTable()
    createUserGroupTable()
    createSocketSessionTable()

def encryptDecryptAlgo(message, encrypted = False):

    if(encrypted):
        # Decrpt the message
        message = message.split("=")
        realMessage = message[0]
        seperator = message[1]
        realMessage = realMessage.split(seperator)
        message = ""

        for word in realMessage:
            if(word):
                message += chr(int(word))

        return message

    else:
        # encrypt the message
        randomKey = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 7))
        enMessage = ""
        for i in message:
            enMessage += str(ord(i))+randomKey
        enMessage+="="+randomKey

        return enMessage


def makePasswordEncrypted(password) -> string:
    return encryptDecryptAlgo(message=password)
     
def makeMessageEncrypted(message) -> string:
    return encryptDecryptAlgo(message=message)

def decryptMessage(encryptedMessage) -> string:
    return encryptDecryptAlgo(message=encryptedMessage, encrypted=True)

def saveDataToTable(tableName, data):
    pass

def createOrUpdateUserSocket(sid, email):
    tableName = "socket_sessions"
    user = database.findBy(table_name="users", column_name='email', column_value=email)
    oldSession = database.findBy(table_name=tableName, column_name='user_id', column_value=user['id'])
    dataToSave = {
        "socket_id" : sid,
        "user_id" : user['id'],
        "created_at" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at" : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    database.inisertData(table=tableName, data=dataToSave)

# def selectFromTable(tableName):
#     data = database.selectAllFromTable(tableName)
#     return data

def checkPassword(encrypted_password, password):
    return encryptDecryptAlgo(encrypted_password, encrypted=True) == password




##########################################
##              SOCKET SCRIPT           ##
##########################################

# # create a Socket.IO server
sio = socketio.Server(logger=True, engineio_logger=True)

# # wrap with a WSGI application
app = socketio.WSGIApp(sio)
# print(socket.socket)

# app = socketio.WSGIApp(sio, static_files={
#     '/': {'content_type': 'text/html', 'filename': 'index.html'}
# })

# Catch every event whichi is occuring
# @sio.on('*')
# def catch_all(event, sid, data):
#    print(event, sid, data)


@sio.event
def connect(sid, environ, auth):
    print('connect ', sid)


# Register event
@sio.event
def register(sid, data):

    try:
        tableName = "users"
        tableAction = database.findFrom(table_name=tableName)
        tableAction.where('email', data['email'])
        tableAction.orWhere('user_name', data['user_name'])
        preUserData = database.getFromQuery(tableAction.getQuery(), only_one_record=True)
        # database.where('email')
        if(preUserData != None):
            sio.emit('errorMessage', data={
                "success" : False,
                "message" : "This Email or Username has already been taken,\n please registered with different or login with the account"
            }, to=sid)
            return 

        dataToSave = {
            "first_name" : data['first_name'],
            "last_name" : data['last_name'],
            "user_name" : data['user_name'],
            "email" : data['email'],
            "is_logged_in" : "0",
            "password" : makePasswordEncrypted(data['password']),
            "created_at" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at" : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        database.inisertData(table=tableName, data=dataToSave)

    except BaseException as error:
        print('An exception occurred: {}'.format(error))
        
        sio.emit("errorMessage", {
            "status" : False,
            "message" : "There seems to be some error, please try later"
        }, to=sid)

        return 
    
    sio.emit("register", {
        "success" : True,
        "message" : "You are registered successfully, go to login page."
    }, to=sid)

# Login event
@sio.event
def login(sid, data):
    try:
        if(data['user_name'] == None or data['password'] == None):
            sio.emit('errorMessage', data={
                "success" : False,
                "Message" : "Please Provide credentials."
            }, to=sid)
            return
        
        tableActions = database.findFrom("users")
        tableActions.where('email', data['user_name'])
        tableActions.orWhere('user_name', data['user_name'])

        user = database.getFromQuery(tableActions.getQuery(), True)
        print(user)
        if user == None:
            sio.emit('errorMessage', {
                "success" : False,
                "message" : "No user find with these credentials."
            }, to=sid)
            return 

        if(checkPassword(encrypted_password=user['password'] , password=data['password']) == False):
            sio.emit('errorMessage', {
                'success' : False,
                "message" : "Entered Password is wrong."
            }, to=sid)
            return
        
        updateTable = database.updateIn(table_name="users")
        updateTable.updateColumn("is_logged_in", 1)
        updateTable.updateOn(column_name="id", column_value=user['id'])
        database.executeUpdate(query=updateTable.getUpdateQuery())
        user = database.getFromQuery(tableActions.getQuery(), True)
        
        sio.emit('login', data={
            'user' : user,
            "success" : True,
            "message" : "You are logged in successfully."
        }, to=sid)

    except BaseException as error:
        print('An exception occurred During Login: {}'.format(error))
        sio.emit('errorMessage', {
            "success" : False,
            "message" : "There seems to be some error, Please try later!"
        }, to=sid)

@sio.on('list_of_users')
def listOfUsers(sid, data):
    tableName = "users"
    fetchedData = database.selectAllFromTable(tableName)
    sio.emit('list_of_users', data=fetchedData, to=sid)

@sio.on('list_of_groups')
def listOfPublicGroup(sid, data):
    tableName = "groups"
    fetchedData = database.selectAllFromTable(tableName)
    sio.emit('list_of_groups', data={
        "success" : True,
        "message" : "List of Users",
        "users" : fetchedData
    }, to=sid)

# User will join a room
@sio.on('join_group')
def joinGroup(sid, data):
    print(data)

@sio.on('group_all_message')
def groupAllMessage(sid, data):
    print(data)


@sio.on('private_message')
def privateMessage(sid, data):
    # sio.emit('pritvat_message')
    print(data)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    createDatabaseTables()
    eventlet.wsgi.server(eventlet.listen(('127.0.0.1', 5000)), app)