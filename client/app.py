import re
import kivy
import socketio

kivy.require('2.0.0') # replace with your current kivy version !


from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup

sio = socketio.Client(logger=True, engineio_logger=True)
host_url = 'http://localhost:5000'
sm = ScreenManager()
back_screen = "main_screen"
socket_connected = False
user = False

class Helper:
    def goBack(self, instance):
        sm.current = back_screen

    def addWidget(self, *widgets):
        for widget in widgets:
            self.add_widget(widget)
    def validateEmptyFields(self, **fields):
        for mainfields in fields:
            for key in fields[mainfields]:
                value = fields[mainfields][key]
                if(value == None or value == ""):
                    
                    error_key = key+"_error"
                    fieldName = " ".join(key.split("_"))
                    return error_key
        return False

    def checkLengthOfFields(self, **fields):
        for key in fields:
            value = fields[key]
            if(value.__len__() < 3 or value.__len__() > 30):
                error_field = key+"_error"
                fieldName = " ".join(key.split("_"))
                return error_field
                # self.error_field.text = f"""{fieldName} must be greater than 3 and less than 30."""

        return False

    def validatePassword(self, **passwords):
        for key in passwords:
            value = passwords[key]
            error_field = key+"_error"
            fieldName = " ".join(key.split("_"))
            
            if(value == None or value ==""):
                # self.error_field.text = f"""{fieldName} is required."""
                return error_field
            elif(value.__len__() < 8 or value.__len__() > 30):
                # self.error_field.text = f"""{fieldName} must be greater than 3 and less than 30."""
                return error_field
        
        return False

    def showMessage(self, data):
        Helper.popUpMessage(message=data['message'])
    def validEmail(self, email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        # and the string into the fullmatch() method
        if(re.fullmatch(regex, email)):
            return True
        else:
            return False
    
    @staticmethod
    def showErrorMessage(data):
        Helper.popUpMessage(data['message'])

    @staticmethod
    def popUpMessage(message):
        popup = Popup(title='Message', content=Label(text=str(message)), size_hint=(None, None), size=(400, 400))
        # create content and add to the popup
        # content = Button(text='Close me!')
        # popup = Popup(content=content, text=,auto_dismiss=False)

        # bind the on_press event of the button to the dismiss function
        # content.bind(on_press=popup.dismiss)

        # open the popup
        popup.open()

class socketController(Helper):

    def __init__(self, url) -> None:
        self.url = url
        sio.connect(url)

    def startSocket(self):
        sio = socketio.Client(logger=True, engineio_logger=True)
    def disconnectSocket(self):
        sio.disconnect()

    def emitEvent(eventName, data):
        sio.emit(event=eventName, data=data)

    def startListingEvents(self):
        sio.on("errorMessage", handler=Helper.showErrorMessage)


class MainScreen(GridLayout, Helper):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.cols = 1
        self.name = "main_screen"
        # self.size_hint = [.5, .5]
        # self.pos_hint = {"top" : .5, "right": .5}
        self.padding = 50
        mainLable = Label(text="Welcome to Quick Chat!", font_size='30')
        loginBtn = Button(text="Login", size_hint=[.5, .25])
        registrationBtn = Button(text="Registration", size_hint=[.5, .25])
        loginBtn.bind(on_press=self.login_callback)
        registrationBtn.bind(on_press=self.registration_callback)
        self.add_widget(mainLable)
        self.add_widget(loginBtn)
        self.add_widget(registrationBtn)
    
    def login_callback(self, instance):
        currentScreen = "login_screen"
        print(instance, currentScreen)
        sm.current = currentScreen
        
    def registration_callback(self, instance):
        currentScreen = "registration_screen"
        back_screen = sm.current_screen
        sm.current = currentScreen

class RegisterScreen(GridLayout, Helper):
    def __init__(self, **kwargs) -> None:
        super(RegisterScreen, self).__init__(**kwargs)
        back_screen = sm.current_screen
        self.padding = 70
        self.cols = 3
        self.spacing = 3

        self.first_name_lable = Label(text='First Name', size_hint=[.5, .25])
        self.first_name = TextInput(multiline=False, size_hint=[.5, .25])
        self.first_name_error = Label(text="",size_hint=[.5, .25], color="#FF0000")

        self.last_name_label = Label(text='Last Name', size_hint=[.5, .25])
        self.last_name = TextInput(multiline=False, size_hint=[.5, .25])
        self.last_name_error = Label(text="",size_hint=[.5, .25], color="#FF0000")

        self.user_name_label = Label(text='User Name', size_hint=[.5, .25])
        self.user_name = TextInput(multiline=False, size_hint=[.5, .25])
        self.user_name_error = Label(text="", size_hint=[.5, .25], color="#FF0000")

        self.email_lable = Label(text='Email', size_hint=[.5, .25])
        self.email = TextInput( multiline=False, size_hint=[.5, .25])
        self.email_error = Label(text="", size_hint=[.5, .25], color="#FF0000")

        self.password_label = Label(text='Password', size_hint=[.5, .25])
        self.password = TextInput(password=True, multiline=False, size_hint=[.5, .25])
        self.password_error = Label(text="", size_hint=[.5, .25], color="#FF0000")

        self.confirm_password_lable = Label(text="Confirm Password", size_hint=[.5, .25])
        self.confirm_password = TextInput(password = True, multiline = False, size_hint = [.5, .25])
        self.confirm_password_error = Label(text="", size_hint=[.5, .25], color="#FF0000")
        
        submit_button = Button(text="Submit", size_hint=[.5, .25])
        go_back = Button(text="Go Back", size_hint=[.5, .25])

        submit_button.bind(on_press=self.makeMyRegistration)
        go_back.bind(on_press=self.goBack)

        self.addWidget(
            self.first_name_lable, 
            self.first_name, 
            self.first_name_error, 
            self.last_name_label, 
            self.last_name,
            self.last_name_error, 
            self.user_name_label, 
            self.user_name, 
            self.user_name_error,
            self.email_lable, 
            self.email, 
            self.email_error,
            self.password_label, 
            self.password, 
            self.password_error,
            self.confirm_password_lable,
            self.confirm_password,
            self.confirm_password_error,
            submit_button,
            go_back
        )

    def makeMyRegistration(self, instance):
        # sio.emit('registeration')
        first_name =  self.first_name.text
        last_name =  self.last_name.text
        user_name =  self.user_name.text
        password =  self.password.text
        confirm_password =  self.confirm_password.text
        email =  self.email.text

        userData = {
            "first_name" : first_name,
            "last_name" : last_name,
            "user_name" : user_name,
            "email" : email,
            "password" : password,
            "confirm_password" : confirm_password,
        }

        anyError = self.validateEmptyFields(fields=userData)
        if(anyError):
            self.adjustError(anyError, "This field is required")
            return 
        anyError = self.checkLengthOfFields(fields=userData)
        if(anyError):
            self.adjustError(errorKey=anyError, message="This must be in the size of 3 to 30")
            return 

        if(password != confirm_password):
            self.adjustError("password_error", "confirm password must be same as the password")
            return
        
        if(self.validEmail(email=email) == False):
            self.adjustError("email_error", "This is not a valid email address")
            return
        
        
        sio.emit('register', userData)
        sio.on('register', self.showMessage)

    
    def adjustError(self, errorKey, message = "somthing wrong with this field"):
        error_values = {
            'first_name_error' : self.first_name_error,
            "last_name_error" : self.last_name_error,
            "user_name_error" : self.user_name_error,
            "email_error" : self.email_error,
            "password_error" : self.password_error,
            "confirm_password_error" : self.confirm_password_error
        } 

        for key in error_values:
            if key == errorKey:
                error_values[key].text = message
            else:
                error_values[key].text = ""

class LoginScreen(GridLayout, Helper):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.padding = 100
        self.cols = 3
        self.spacing = 3
        self.spacing = 5
        user_name_label = Label(text='User Name', size_hint=[.25, .25])
        self.user_name = TextInput(multiline=False, size_hint=[.25, .25], font_size=30)
        self.user_name_error = Label(text="", size_hint=[.25, .25], color="#FF0000")

        password_label = Label(text='password', size_hint=[.25, .25])
        self.password = TextInput(password=True, multiline=False, size_hint=[.25, .25])
        self.password_error = Label(text="", size_hint=[.25, .25], color="#FF0000")

        submit_button = Button(text="Submit", size_hint=[.25, .25])
        go_back = Button(text="Go Back", size_hint=[.25, .25])

        submit_button.bind(on_press=self.makeLogin)
        go_back.bind(on_press=self.goBack)

        self.addWidget(
            user_name_label,
            self.user_name,
            self.user_name_error,
            password_label,
            self.password,
            self.password_error,
            submit_button,
            go_back
        )

    def makeLogin(self, instance):
        userData = {
            'user_name' : self.user_name.text,
            "password" : self.password.text
        }

        anyError = self.validateEmptyFields(fields=userData)
        if(anyError):
            self.adjustError(anyError, "This field is required")
            return 
        
        # anyError = self.checkLengthOfFields(fields=userData)
        # if(anyError):
        #     self.adjustError(errorKey=anyError, message="This must be in the size of 3 to 30")
        #     return 
        
        sio.emit('login', data=userData)
        sio.on('login', self.handleLogin)
    
    def handleLogin(self, data):
        print(data, "FROM Handle Login")
        user = data['user']
        back_screen = sm.current_screen
        sm.current = "users_screen"
    
    def adjustError(self, errorKey, message = "somthing wrong with this field"):
        error_values = {
            "user_name_error" : self.user_name_error,
            "password_error" : self.password_error
        } 

        for key in error_values:
            if key == errorKey:
                error_values[key].text = message
            else:
                error_values[key].text = ""


class UsersScreen(GridLayout, Helper):
    def __init__(self,**kwargs):
        super(UsersScreen, self).__init__(**kwargs)
        self.padding = 70
        data = {
            "table" : "users"
        }
        sio.emit('list_of_users', data=data)
        sio.on('list_of_users', handler=self.markUsers)

    def markUsers(self, data):
        for user in data['users']:
            userBtn = Button(text=(user['user_name']), size_hint=[.25, .25])
            userBtn.bind(self)
            self.add_widget(userBtn)
    def showChat(self, instance):
        print(instance.text)
        pass
class GroupScreen():
    pass
class ChatScreen():
    pass
class GroupChatScreen():
    pass

SCREENS = {
    "main_screen":MainScreen,
    "login_screen" : LoginScreen,
    "registration_screen" : RegisterScreen,
    # "group_chat_screen" : GroupChatScreen,
    'users_screen' : UsersScreen,
    # 'chat_screen' : ChatScreen,
    # 'user_screen' : UsersScreen
}



class MyApp(App):

    def build(self):
        
        for key in SCREENS:
            page = SCREENS[key]()
            print(key)
            screen = Screen(name=key)
            screen.add_widget(page)
            sm.add_widget(screen=screen)

        return sm


if __name__ == '__main__':
    socket = socketController(host_url)
    socket.startSocket()
    socket.startListingEvents()
    MyApp().run()
