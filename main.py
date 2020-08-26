from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.config import Config
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout

import os
import time
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '600')

# Login window
class LoginWin(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    
    def loginBtn(self):
        if self.checkValid():
            pass
            screens[ "Main"]=MainWindow(name="Main")
            sm.add_widget(screens["Main"])
            sm.current="Main"
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


class MainWindow(Screen):
    _Camera = ObjectProperty(None)
    img_Button=ObjectProperty(None)
    _Again_Button=ObjectProperty(None) 

    def Camera(self):
        print("Hi")
        if self.img_Button.text=='Camera':
            Show_Widget(self._Camera)
            Hide_Widget(self._Again_Button)
            self._Camera.play = True
            self.img_Button.text='Take a Photo'
            pass
        elif  self.img_Button.text=='Take a Photo':
            self._Camera.play=False
            self.img_Button.text= 'Analysis'    
            Show_Widget(self._Again_Button)

        elif self.img_Button.text=='Analysis':

            self.img_Button.text= 'Camera'
            timestr = time.strftime("%Y%m%d_%H%M%S")
            self._Camera.export_to_png("IMG_{}.png".format(timestr))
            print("Captured")
            Hide_Widget(self._Again_Button)
            # Hide_Widget(self._Camera)
            self._Camera.opacity=0    

    def Again(self):
        self._Camera.play=True
        Hide_Widget(self._Again_Button)
        self.img_Button.text='Take a Photo'

    def Change_Camera(self):
        try:
            self._Camera.index=int(not self._Camera.index)
        except:
            pass
    # def Gallery(self):
    #     Image(source="ali.png").canvas

def Hide_Widget(widget):
    widget.opacity=0    
    widget.disabled = True

def Show_Widget(widget):
    widget.opacity=1
    widget.disabled = False


# windows manager
class WindowManager(ScreenManager):
    pass



Builder.load_file("./loginPart/login.kv")
Builder.load_file("./signUpPart/signUp.kv")
Builder.load_file("./MainWindow/Mainwindow.kv")

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
