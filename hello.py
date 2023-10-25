from flask import Flask
import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy import String,Integer
from sqlalchemy.orm import Mapped

from sqlalchemy.sql import func
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ="mysql://root:Your_Password_here@localhost:3306/users"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(20))
    password: Mapped[str] = mapped_column(String(20))

with app.app_context():
    db.create_all()

# @app.route('/')
# def hello():
#     conn = mysql.connect()
#     cursor =conn.cursor()

#     return data