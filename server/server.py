import socketio

# # create a Socket.IO server
sio = socketio.Server(logger=True, engineio_logger=True)

# # wrap with a WSGI application
# app = socketio.WSGIApp(sio)
# print(socket.socket)

# create a Socket.IO server
# sio = socketio.AsyncServer()

# # wrap with ASGI application
# app = socketio.ASGIApp(sio)
# print(app)

print(sio)


# Catch every event whichi is occuring
@sio.on('*')
def catch_all(event, sid, data):
   print(event, sid, data)



# @sio.on('connect')
# async def on_connect(sid, environ, data):
#     print(sid, data)

@sio.event
def connect(sid, environ, auth):
    print('connect ', sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

@sio.on('private_message')
def privateMessage(sid, data):
    print(data)


@sio.on('room_message')
def roomMessage(sid, data):
    print(data)
    sio.emit('room_message',data, room="room_name")