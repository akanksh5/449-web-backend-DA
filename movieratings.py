from flask import Flask, request, redirect, jsonify,abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase,mapped_column, Mapped
from sqlalchemy import String,Integer
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required,JWTManager
from werkzeug.utils import secure_filename
from os import environ 
import os
import werkzeug 

from sqlalchemy.sql import func
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =environ.get('SQLALCHEMY_DATABASE_URI')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =environ.get('SQLALCHEMY_TRACK_MODIFICATIONS') 
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

app.config['UPLOAD_FOLDER'] = environ.get('UPLOAD_FOLDER')

db.init_app(app)

class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(20))
    password: Mapped[str] = mapped_column(String(20))

class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(20), nullable=False)
    moviename: Mapped[str] = mapped_column(String(20),nullable=False)
    rating:  Mapped[int] = mapped_column(Integer)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = environ.get("JWT_SECRET_KEY")  # Change this!
jwt = JWTManager(app)

# Create all the tables in the database
with app.app_context():
    db.create_all()


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    obj =User.query.filter_by(username=username,password=password).first()
    if username == None or password == None:
        return jsonify({"msg": "username or password is missing"}), 400
    if obj:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "invalid username or password"}), 401

# function that returns the allowed file extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function that's used to register the users
@app.route('/register', methods = [ 'POST']) #Create
def registeruser():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    email = request.json.get("email", None)
    if username == None:
        return "username is absent",404
    user = User(username=username,password=password,email=email)
    db.session.add(user)
    db.session.commit()
    return "The user has been registered",201


# The public route that displays the list of movie reviews submitted by all the users
@app.route('/movies')
def showmovies():
    movies = Movie.query.filter().all()
    result = []
    for i in movies:
        result.append({'Movie Name':i.moviename,'Rating':i.rating,'Username':i.username})
    return jsonify({'Movies':result}), 200

# endpoint used to create a movie rating entry by an authenticated user

@app.route('/movie', methods = [ 'POST']) #Create
@jwt_required()
def createmovie():
   #username=request.json.get("username", None)
    moviename = request.json.get("moviename", None)
    movierating = request.json.get("movierating", 0)
    current_user = get_jwt_identity()
    if moviename == None:
        return "movie name is absent",404
    movie = Movie(username=current_user,moviename=moviename,rating=movierating)
    db.session.add(movie)
    db.session.commit()
    return "the movie record has been created", 201


# endpoint used to read a movie rating entry by an authenticated user
@app.route('/movie/<movieName>', methods = ['GET']) #Read
@jwt_required()
def getmovie(movieName):
    current_user = get_jwt_identity()
    obj =Movie.query.filter_by(username=current_user,moviename=movieName).first_or_404()
    result={'Movie Name':obj.moviename,'Rating':obj.rating,'Username':obj.username}
    return jsonify({'Movies':result})


# endpoint used to update a movie rating entry by an authenticated user
@app.route('/movie/<moviename>', methods = ['PUT']) #Update
@jwt_required()
def updatemovie(moviename):
    movierating = request.json.get("movierating", 0)
    current_user = get_jwt_identity()
    if moviename == None:
        return "movie name is absent",404
    movie = Movie.query.filter_by(username=current_user,moviename=moviename).update(dict(rating=movierating))
    db.session.commit()
    return "the movie record has been updated",201

# endpoint used to delete a movie rating entry by an authenticated user
@app.route('/movie/<moviename>', methods = ['DELETE']) #Delete
@jwt_required()
def deletemovie(moviename):
    current_user = get_jwt_identity()
    obj =Movie.query.filter_by(username=current_user,moviename=moviename).first()
    db.session.delete(obj)
    db.session.commit()
    return "the movie record has been deleted!",204

# endpoint used to upload a file by an authenticated user
@app.route('/uploader', methods = ['GET', 'POST'])
@jwt_required()
def upload_file():
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
        return 'file uploaded successfully',204
     
# Error handler functions
@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    return 'Bad request!', 400

     
@app.errorhandler(werkzeug.exceptions.Unauthorized)
def handle_unauthorized_request(e):
    return 'Unauthorized request!', 401

     
@app.errorhandler(werkzeug.exceptions.NotFound)
def handle_bad_request(e):
    return 'Resource not found!', 404

     
@app.errorhandler(werkzeug.exceptions.InternalServerError)
def handle_internal_server_error_request(e):
    return 'Internal Server Error', 500
