import socketio



# standard Python
sio = socketio.Client(logger=True, engineio_logger=True)


@sio.on('my message')
def on_message(data):
    print('I received a message!')

# @sio.on('*')
# def catch_all(event, data):
#     pass

@sio.event
def connect():
    print("I'm connected!")

@sio.event
def connect_error(data):
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")

sio.connect('http://localhost:5000')

print('my sid is', sio.sid)

sio.emit('my message', {'foo': 'bar'}, namespace='/chat')

# sio.disconnect()

# sio.wait()
# def my_background_task(my_argument):
#     # do some background work here!
#     pass

# task = sio.start_background_task(my_background_task, 123)