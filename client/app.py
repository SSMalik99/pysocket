import kivy
kivy.require('2.0.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen

class MainScreen(GridLayout):
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
        
    def registration_callback(self, instance):
        print("registration", instance)

class RegisterScreen():
    pass
class UsersScreen():
    pass
class GroupScreen():
    pass
class ChatScreen():
    pass
class GroupChatScreen():
    pass
class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.name = "login_screen"
        self.cols = 2
        self.add_widget(Label(text='User Name'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text='password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)
        submit_button = Button(text="Submit")
        self.add_widget(submit_button)



sm = ScreenManager()

SCREENS = {
    "main_screen":MainScreen,
    "login_screen" : LoginScreen,
    "registration_screen" : RegisterScreen,
    "group_chat_screen" : GroupChatScreen,
    'user_screen' : UsersScreen,
    'chat_screen' : ChatScreen,
    'user_screen' : UsersScreen
}

for key in SCREENS:
    screen = Screen(name=key)
    sm.add_widget(screen)

class MyApp(App):
    def changeScreen(screenName):
        currentScreen = MyApp.SCREENS[screenName]()
        
    def build(self):

        sm = ScreenManager()
        sm.current = "main_screen"
        return sm
        # return LoginScreen()


if __name__ == '__main__':
    MyApp().run()