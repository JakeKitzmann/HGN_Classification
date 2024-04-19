import firebase_admin   # pip install firebase_admin
from firebase_admin import db as firebase_db, credentials
from flask import Flask, render_template, request

# Initialize Flask app
app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred)

@app.route('/')
def index():
    return render_template('index.html')



