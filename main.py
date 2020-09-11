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
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import AsyncImage


from database import _request_

import threading

import os
import time


Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '800')


try:
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.INTERNET,Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE,Permission.CAMERA])
except:
    pass


# Login window
class LoginWin(Screen):
    email = ObjectProperty()
    password = ObjectProperty()
    userMsg = ObjectProperty()

    @mainthread
    def loginBtn(self):
        if self.checkValid():
            # checkExist = 1
            checkExist = _request_.login(email=self.email.text.strip(), password= self.password.text.strip())
            if checkExist == 1:
                screens["Main"] = MainWindow(name="Main")
                sm.add_widget(screens["Main"])
                sm.current = "Main"
            elif checkExist == 0:
                self.userMsg.text = "Email or password wrong"
                self.error(clr=True)
            elif checkExist == -1:
                self.userMsg.text = "Connection failed"
                self.error(clr=True)

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
    def error(self, color=(1, 0, 0, 0.4), Hide=False, clr=False):
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
    # lName = ObjectProperty()
    _CheckBox_Doctor = ObjectProperty()
    _Label_Doctor = ObjectProperty()
    _DoctorID = ObjectProperty()

    @mainthread
    def submitBtnUser(self):
        if self.checkValid() == 1:
            info = {}
            info['email'] = self.email.text.strip()
            info['FullName'] = self.fName.text.strip()
            info['password'] = self.password.text.strip()
            info['phone'] = self.phoneNum.text.strip()
            info['doctor_id'] = self._DoctorID.text.strip()
            info['is_doctor'] = self._CheckBox_Doctor.active
            check = _request_.signUp(**info)
            if check == 1:
                if self._CheckBox_Doctor.active:
                    self.userMsg.text = "Please wait to verify your doctor ID"
                    self.error(clr=True)
                else:
                    self.userMsg.text = "You have registered. Enjoy this app "
                    self.error()
            elif check == -2:
                self.userMsg.text = "you has been regestered before"
                self.error(clr=True)
            elif check == -1:
                self.userMsg.text = "Connection failed"
                self.error(clr=True)
            elif check == 0:
                self.userMsg.text = "Invalid information"
                self.error(clr=True)

        elif self.checkValid() == -1:
            self.userMsg.text = "Passwords are not equal"
            self.error([self.r_password], clr=True)

        elif self.checkValid() == -2:
            self.userMsg.text = "Password's length must be more than 6 characters"
            self.error([self.password, self.r_password], clr=True)
        else:
            self.userMsg.text = "Fill all with correct value please"
            self.error([self.password, self.r_password,
                        self.email, self.phoneNum], clr=False)


    def Doctor(self):
        if self._CheckBox_Doctor.active:
            self._Label_Doctor.opacity = 0
            self._DoctorID.opacity = 1
        else:
            self._Label_Doctor.opacity = 1
            self._DoctorID.opacity = 0
    # handle error to users

    @mainthread
    def error(self, textInputs=[], color=(1, 0, 0, 0.4), Hide=False, clr=False):
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
        if self.email.text.strip() and self.phoneNum.text.strip() and self.password.text.strip() and self.r_password.text.strip() and self.fName.text.strip():
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
    img_Button = ObjectProperty()
    _Again_Button = ObjectProperty()
    _Gallery_Button = ObjectProperty(None)
    lbl_path = ObjectProperty(None)
    img_Gallery = ObjectProperty(None)
    picture_path = ""

    def Camera(self):

        if self.img_Button.source == './icon/camera.png':
            self._Camera.opacity = 1
            Hide_Widget(self.img_Gallery)
            Show_Widget(self._Camera)
            Hide_Widget(self._Again_Button)
            self._Camera.play = True
            self.img_Button.source = './icon/takePhoto.png'

        elif self.img_Button.source == './icon/takePhoto.png':
            self._Camera.play = False
            self.img_Button.source = './icon/analysis.png'
            Show_Widget(self._Again_Button)

        elif self.img_Button.source == './icon/analysis.png':
            if self._Camera.opacity == 1:
                timestr = time.strftime("%Y%m%d_%H%M%S")
                if not os.path.isfile('/sdcard/Medical Project'):
                    os.mkdir("/sdcard/Medical Project")
                self._Camera.export_to_png(
                    "/sdcard/Medical Project/IMG_{}.png".format(timestr))
            else:
                self.picture_path = self.img_Gallery.source
                self.lbl_path.text = self.picture_path
                check = _request_.postImage(path = self.img_Gallery.source)
                if check:
                    self.lbl_path.text = "Done"
                else:
                    "connection failed"


            self.img_Button.source = './icon/camera.png'
            Hide_Widget(self._Again_Button)
            Show_Widget(self._Gallery_Button)
            self._Camera.opacity = 0

    def Again(self):
        self._Camera.play = True
        self.img_Button.source = './icon/takePhoto.png'
        Hide_Widget(self._Again_Button)
        Hide_Widget(self.img_Gallery)
        self._Camera.opacity = 1

    def show_load(self):
        self._Camera.play = False
        self._Camera.opacity = 0
        screens["GalleryCamera"] = Gallery(name="GalleryCamera")
        sm.add_widget(screens["GalleryCamera"])
        sm.current = "GalleryCamera"

    def dismiss_popup(self):
        self._popup.dismiss()
        Hide_Widget(self._Again_Button)
        self.img_Button.source = './icon/camera.png'


    def load(self, path):
        with open(path):
            self.img_Gallery.source = path
        self.img_Gallery.opacity = 1
        self.img_Button.source = './icon/analysis.png'
        Show_Widget(self._Again_Button)




class Gallery(BoxLayout, Screen):
    def __init__(self, _source= "/home/mehdi/Pictures", *args, **kwargs):
        super(Gallery, self).__init__(*args, **kwargs)
        self._source = _source
        self.callback()

    def callback(self):
        def update_height(img, *args):
            img.height = img.width / img.image_ratio


        imgs = []
        valid_Format = ['png', 'jpg', 'jpeg']
        
        for img in os.listdir(self._source):
            if img.split(".")[-1] in valid_Format:
                imgs.append(os.path.join(self._source, img))


        for img in imgs:
            image = _AsyncImage(source=img,
                               size_hint=(1, None),
                               keep_ratio=True,
                               allow_stretch=True)
            image.bind(width=update_height, image_ratio=update_height)
            self.ids.wall.add_widget(image)


    def closeGallery(self):
        sm.current = "Main"

    def chooseDir(self, text= None):
        screenName = "Gallery" + text
        paths = {}
        paths["GalleryCamera"] = "/home/mehdi/Pictures"
        paths["GalleryScreenShut"] = "/home/mehdi/Pictures"
        paths["GalleryDownload"] = "/home/mehdi/Pictures/Wallpapers"
        paths["GalleryTelegram"] = "/home/mehdi/Pictures/Wallpapers"

        if not sm.current == screenName:
            screens[screenName] = Gallery(name=screenName, _source= paths[screenName])
            sm.add_widget(screens[screenName])
            sm.current = screenName
            
        else:
            pass 



class _AsyncImage(AsyncImage):
    def __init__(self, *args, **kwargs):
        super(_AsyncImage, self).__init__(*args, **kwargs)

    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print(self.source)
            ChoosenImgPath.update({"path": self.source})
            try:
                sm.remove_widget(screens["FullImage"])
            except Exception as e:
                print(e)
                pass
            screens["FullImage"] = FullImageView(name= "FullImage", _source= self.source)
            sm.add_widget(screens["FullImage"])
            sm.current = "FullImage"



class FullImageView(Screen):

    def __init__(self, name= None, _source= None, *args, **kwargs):
        Screen.__init__(self, name= name)
        self.ids.img.source = _source

    def back(self):
        sm.current = "GalleryCamera"

    def selectImage(self):
        sm.current = "Main"
        sm.get_screen("Main").load(path=ChoosenImgPath["path"])


ChoosenImgPath = {"path": None}


def Hide_Widget(widget):
    widget.opacity = 0
    widget.disabled = True


def Show_Widget(widget):
    widget.opacity = 1
    widget.disabled = False


# windows manager
class WindowManager(ScreenManager):
    pass


Builder.load_file("./loginPart/login.kv")
Builder.load_file("./signUpPart/signUp.kv")
Builder.load_file("./MainWindow/Mainwindow.kv")

# create windowsmanager and handle screens
sm = WindowManager()
screens = {"login": LoginWin(name="login"),
           "signUser": SignwinUser(name="signUser")}
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
