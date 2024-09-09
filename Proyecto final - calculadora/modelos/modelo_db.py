import firebase_admin
from firebase_admin import credentials, db
#inicia la base de datos
cred = credentials.Certificate("modelos\calculadora-grafica-86c61-firebase-adminsdk-42myb-2046c04d59.json")
firebase_admin.initialize_app(cred, {'databaseURL':'https://calculadora-grafica-86c61-default-rtdb.firebaseio.com/'})