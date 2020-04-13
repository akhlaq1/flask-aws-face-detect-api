from pyrebase import pyrebase
from datetime import datetime

import ntpath



config = {
  "apiKey": "AIzaSyBUiyeRA34zb435kpZALSIRD9TdLB4N7I8",
  "authDomain": "angular-ml-chen.firebaseapp.com",
  "databaseURL": "https://angular-ml-chen.firebaseio.com",
  "projectId": "angular-ml-chen",
  "storageBucket": "angular-ml-chen.appspot.com",
  "messagingSenderId": "766726268244",
  "appId": "1:766726268244:web:120cbcc0fb85f9f3fdd4c1",
  "measurementId": "G-4R2DF3XPBF"
} 

firebase = pyrebase.initialize_app(config)

global storage
storage = firebase.storage()

def upload_img(output_img_path):

    now = datetime.now()
    date_time = now.strftime("%H:%M:%S")
    
    img_name = ntpath.basename(output_img_path)

    img_name = "images/"+date_time+img_name
    storage.child(img_name).put(output_img_path)
    img_url = storage.child(img_name).get_url(None)
    return img_url

