from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.config import Config
from kivy.uix.image import Image
from kivy.clock import Clock, mainthread
from kivy.uix.boxlayout import BoxLayout

from database import Database

import threading

import os
import time
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '800')

# Login window
class LoginWin(Screen):
    email = ObjectProperty()
    password = ObjectProperty()
    userMsg = ObjectProperty()

    @mainthread
    def loginBtn(self):
        if self.checkValid():
            checkExist = 1
            # checkExist = Database.userExist(email=self.email.text.strip(), password= self.password.text.strip())
            if checkExist == 1:
                screens["Main"]=MainWindow(name="Main")
                sm.add_widget(screens["Main"])
                sm.current="Main"
            elif checkExist == 0:
                self.userMsg.text = "Email or password wrong"
                self.error(clr= True)
            elif checkExist == -1:
                self.userMsg.text = "Connection failed"
                self.error(clr= True)

        else:
            self.userMsg.text = "Fill all with correct value please"
            self.error()
            

    def checkValid(self):
        if (self.email.text.strip() and self.password.text.strip()):
            return True
        return False


    @mainthread
    def go_signUpUser(self):
        sm.current = "signUser"

    @mainthread
    def error(self, color= (1, 0, 0, 0.4), Hide=False, clr = False):
        if clr:
            self.email.background_color = color
            self.password.background_color = color
        if Hide:
            Hide_Widget(self.userMsg)
        else: 
            Show_Widget(self.userMsg)

    def wait(self):
        time.sleep(6)
        print("done")


    # @mainthread
    # def waitToClear(self, _time= 3):
    #     time.sleep(_time)
    #     Hide_Widget(self.userMsg)





# signUp window for user
class SignwinUser(Screen):
    userMsg = ObjectProperty() 
    email = ObjectProperty()
    password = ObjectProperty()
    r_password = ObjectProperty()
    phoneNum = ObjectProperty()
    fName = ObjectProperty()
    lName = ObjectProperty()
    
    @mainthread
    def submitBtnUser(self):
        if self.checkValid() == 1:
            info = {}
            info['email'] = self.email.text.strip()
            info['FirstName'] = self.fName.text.strip()
            info['LastName'] = self.lName.text.strip()
            info['password'] = self.password.text.strip()
            info['phone'] = self.phoneNum.text.strip()
            info['user_type'] = 'Ordinary person'
            info['regester_type'] = 'App'
            info['doctor_id'] = None
            check = Database.registerOP(**info)

            if check == 1:
                self.userMsg.text = "You have registered. Enjoy this app "
                self.error()
            elif check == 0:
                self.userMsg.text = "you has been regestered before"
                self.error(clr= True)
            elif check == -1:
                self.userMsg.text = "Connection failed"
                self.error(clr= True)


        elif self.checkValid() == -1:
            self.userMsg.text = "Passwords are not equal"
            self.error([self.r_password], clr= True)

        elif self.checkValid() == -2:
            self.userMsg.text = "Password's length must be more than 6 characters"
            self.error([self.password, self.r_password], clr= True)
        else:
            self.userMsg.text = "Fill all with correct value please"
            self.error([self.password, self.r_password, self.email, self.phoneNum], clr= False)

        
    # handle error to users
    @mainthread
    def error(self, textInputs= [], color= (1, 0, 0, 0.4), Hide=False, clr = False):
        if clr:
            for win in textInputs:
                win.background_color = color
        if Hide:
            Hide_Widget(self.userMsg)
        else:
            Show_Widget(self.userMsg)

    @mainthread
    def go_loginWin(self):
        sm.current = "login"


    # handle correctness of textinputs
    def checkValid(self):
        if self.email.text.strip() and self.phoneNum.text.strip() and self.password.text.strip() and self.r_password.text.strip() and self.fName.text.strip() and self.lName.text.strip():
            if self.password.text.strip() == self.r_password.text.strip():
                if len(self.password.text.strip()) > 5:
                    return 1
                else:
                    return -2
            else: 
                return -1
        return 0





class MainWindow(Screen):
    _Camera = ObjectProperty()
    img_Button=ObjectProperty()
    _Again_Button=ObjectProperty() 

    def Camera(self):
        print("Hi")
        if self.img_Button.source=='./icon/camera.png':
            Show_Widget(self._Camera)
            Hide_Widget(self._Again_Button)
            self._Camera.play = True
            self.img_Button.source='./icon/takePhoto.png'
            pass
        elif  self.img_Button.source=='./icon/takePhoto.png':
            self._Camera.play=False
            self.img_Button.source= './icon/analysis.png'    
            Show_Widget(self._Again_Button)

        elif self.img_Button.source=='./icon/analysis.png':

            self.img_Button.source= './icon/camera.png'
            timestr = time.strftime("%Y%m%d_%H%M%S")
            self._Camera.export_to_png("IMG_{}.png".format(timestr))
            print("Captured")
            Hide_Widget(self._Again_Button)
            # Hide_Widget(self._Camera)
            self._Camera.opacity=0    

    def Again(self):
        self._Camera.play=True
        Hide_Widget(self._Again_Button)
        self.img_Button.surce='./icon/takePhoto.png'

    def Change_Camera(self):
        try:
            self._Camera.index=int(not self._Camera.index)
        except:
            pass
    def Gallery(self):
        Image(source="ali.png").canvas

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
