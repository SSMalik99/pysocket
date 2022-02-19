import eventlet
import string
import random
import socketio
import db

dbHost= "127.0.0.1"
dbUser = "root"
dbPassword = "bubby"
dbName = "chat_day"

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
    createdAt = db.TableColumn('created_at')
    updateAt = db.TableColumn('updated_at')

    # define properties for columns
    id.big_int()
    id.nullAble(False)
    
    firstName.string_column()
    
    lastName.string_column()
    lastName.nullAble()

    email.string_column()
    email.uniqueIndex()

    password.string_column()
    password.nullAble(False)

    userName.string_column()
    userName.uniqueIndex()

    createdAt.date_time_column()
    createdAt.nullAble()

    updateAt.date_time_column()
    updateAt.nullAble()
    
    # Make table
    database.makeMyTable(id, firstName, lastName, email, password, userName, createdAt, updateAt)

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
    id.nullAble(False)
    
    socketId.big_int(False)
    userId.big_int(False)

    createdAt.date_time_column()
    createdAt.nullAble()

    updateAt.date_time_column()
    updateAt.nullAble()

    database.makeMyTable(id, socketId, userId, createdAt, updateAt)

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


# # create a Socket.IO server
sio = socketio.Server(logger=True, engineio_logger=True)

# # wrap with a WSGI application
# app = socketio.WSGIApp(sio)
# print(socket.socket)

app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})
# create a Socket.IO server
# sio = socketio.AsyncServer()

# # wrap with ASGI application
# app = socketio.ASGIApp(sio)
# print(app)

# print(sio)


# Catch every event whichi is occuring
@sio.on('*')
def catch_all(event, sid, data):
   print(event, sid, data)


@sio.event
def connect(sid, environ, auth):
    print('connect ', sid)


# Register event
@sio.event
def register(sid, data):
    print(data)

# Login event
@sio.event
def login(sid, data):
    print(data)

@sio.on('list_of_users')
def listOfUsers(sid, data):
    print(data)

@sio.on('list_of_groups')
def listOfPublicGroup(sid, data):
    print(data)

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
    eventlet.wsgi.server(eventlet.listen(('127.0.0.1', 5000)), app)