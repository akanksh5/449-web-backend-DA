
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase,mapped_column, Mapped
from sqlalchemy import String,Integer
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required,JWTManager
from werkzeug.utils import secure_filename
import os

from sqlalchemy.sql import func
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ="mysql://root:PasswordHere!@localhost:3306/users"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
UPLOAD_FOLDER = './files/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(app)

class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(20))
    password: Mapped[str] = mapped_column(String(20))


# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = ""  # Change this!
jwt = JWTManager(app)


with app.app_context():
    db.create_all()

@app.route('/')
def hello():
    return "Hello World!"

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    #db lookup username ->
     #if username not present in db
    username = None
    if username == None:
        return  'bad request!', 400
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
#    if request.method == 'POST':
#       f = request.files['file']
#       f.save(secure_filename(f.filename))
#       return 'file uploaded successfully'
     if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        try:
            os.mkdir(app.config['UPLOAD_FOLDER'])
        except OSError:
            print ("Creation of the directory %s failed" % app.config['UPLOAD_FOLDER'])
        else:
            print ("Successfully created the directory %s " % app.config['UPLOAD_FOLDER'])
        if not allowed_file(file.filename):
            return 'invalid file type uploaded',401
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'file uploaded successfully'