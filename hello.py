from flask import Flask
import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ="mysql://root:Your_Password_Here@localhost:3306/users"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
@app.route('/')
def hello():
    conn = mysql.connect()
    cursor =conn.cursor()

    return data