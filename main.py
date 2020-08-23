from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.config import Config

Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '800')





# Login window
class LoginWin(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    
    def loginBtn(self):
        if self.checkValid():
            print(self.email.text, self.password.text)
        else:
            pupUp_Msg(self, txt= "Fill all with \ncorrect value please")


    def checkValid(self):
        if (self.email.text.strip() and self.password.text.strip()):
            return True
        return False

    

    def go_signUpUser(self):
        sm.current = "signUser"





# signUp window for user
class SignwinUser(Screen):
    
    def submitBtnUser(self):
        if self.checkValid() == 1:
            print("sign button", self.email.text.strip())
        elif self.checkValid() == -1:
            pupUp_Msg(self, txt="Password in not equal")
        elif self.checkValid() == -2:
            pupUp_Msg(self, txt="Password's length must be \nmore than 8 characters")
        else:
            pupUp_Msg(self, txt="Fill all with \ncorrect value please")



    def go_loginWin(self):
        sm.current = "login"

    # handle correctness of textinputs
    def checkValid(self):
        if self.email.text.strip() and self.phoneNum.text.strip() and self.password.text.strip() and self.r_password.text.strip():
            if self.password.text.strip() == self.r_password.text.strip():
                if len(self.password.text.strip()) > 7:
                    return 1
                else:
                    return -2
            else: 
                return -1
        return 0



# handle invalid form for input text content
def pupUp_Msg(win, txt= ""):
    pop = Popup(title='Invalid Form',
                content=Label(text=txt, 
                font_size= (win.width**2 + win.height**2) / 14.8**4, color= [0.6, 0.2, 0.2, 1]),
                size_hint=(0.5, 0.3))
    pop.open()


# windows manager
class WindowManager(ScreenManager):
    pass



Builder.load_file("./loginPart/login.kv")
Builder.load_file("./signUpPart/signUp.kv")

# create windowsmanager and handle screens
sm = WindowManager()
screens = {"login": LoginWin(name= "login"), "signUser": SignwinUser(name= "signUser")}
sm.add_widget(screens["login"])
for key in screens:
    if key != "login":
        sm.add_widget(screens[key])
sm.current = "login"



class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()
