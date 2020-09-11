import requests
from time import sleep
import os

def login(**kwargs):
    try:
        sleep(2)
        url = "http://127.0.0.1:8000/api_user/login/"
        data = {
            'username': kwargs["email"],
            'password': kwargs["password"]
        }
        x = requests.post(url, data= data)  
    except Exception as e:
        return -1    

    try:
        if x.json()['token']:
            open (os.path.join(os.getcwd(), "token.txt"), 'w').write(x.json()['token'])
            return 1
    except Exception as e:
        print(e)
        return 0



def signUp(**kwargs):
    try:
        url = "http://127.0.0.1:8000/api_user/register/"
        data = {
            'email': kwargs["email"],
            'phone_number': kwargs["phone"],
            'password': kwargs["password"],
            'full_name': kwargs["FullName"],
            'register_type': "app_register",
            'is_doctor': kwargs["is_doctor"],
            'doctor_id': kwargs["doctor_id"],
        }
        x = requests.post(url, data= data)
    except Exception as e:
        print(e)
        return -1

    try:
        if x.json()['email'][0] == 'user with this email already exists.':
            return -2
    except:
        pass

    try:
        if x.json()['response'] == 'successfully registered a new user':
            return 1
    except:
        return 0


def postImage(path= None):
    try:
        url = "http://127.0.0.1:8000/api_image/create/"
        files = {'pic': open(path, 'rb')}
        token = open (os.path.join(os.getcwd(), "token.txt")).read()
        print(token)
        headers = {
            'Authorization' : f'token {token}'
        }
        x = requests.post(url, files= files, headers= headers)
        print(x.json())
        return 1
    except Exception as e:
        return 0




