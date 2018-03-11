import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import aspect_model
import polarity_model

cred = credentials.Certificate('test_area_file/credentialAuth.json')
default_app = firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://moviescorer-67315.firebaseio.com/'
})

data = db.reference('movies').get()
root = db.reference()
movieData = []

#update movie list
for movieKey,movieValue in data.items():
    print("something")