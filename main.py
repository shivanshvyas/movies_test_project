from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import jsonify,json
from flask import request
from flask import jsonify,request,make_response,url_for,redirect,Response
from json import dumps

import requests
from requests import post
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.declarative import declarative_base
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager
from flask import Response, request
from flask_jwt_extended import create_access_token
# from .env import *
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///movies.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
# app.config.from_envvar('ENV_FILE_LOCATION')
Base = declarative_base()
jwt = JWTManager(app)
class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    platform = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    editor_choice = db.Column(db.String(50), nullable=False)
    score = db.Column(db.String(50), nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
    	return f"{self.id} - {self.title}"
    def json(self):
    	return {'id': self.id, 'title': self.title,
                'platform': self.platform, 'genre': self.genre, 'editor_choice': self.editor_choice, 'score': self.score}
        # this method we are defining will convert our output to json

    def add_movie(_title, _platform, _genre,_editor_choice,_score):
    
	    new_movie = Movies(title=_title, platform=_platform, genre=_genre,editor_choice=_editor_choice,score=_score)
	    db.session.add(new_movie)  # add new movie to database session
	    db.session.commit()

    def get_movie(_id):
    	return [Movies.json(Movies.query.filter_by(id=_id).first())]
    def get_all_movies():
    	return [Movies.json(movie) for movie in Movies.query.all()]
      

    def update_movie(_id, _title, _platform,_genre, _editor_choice,_score):
        
        movie_to_update = Movies.query.filter_by(id=_id).first()
        movie_to_update.title = _title
        movie_to_update.platform = _platform
        movie_to_update.genre = _genre
        movie_to_update.editor_choice = _editor_choice
        movie_to_update.score = _score
     
        db.session.commit()


    def delete_movie(_id):
        '''function to delete a movie from our database using
           the id of the movie as a parameter'''
        Movies.query.filter_by(id=_id).delete()
        # filter movie by id and delete
        db.session.commit()  # commiting the new change to our database


class User(Base):
	__tablename__ = 'USER'
	user_id = db.Column(db.Integer)
	account_number = db.Column(db.String(8), primary_key=True, nullable=False)

	email =  db.Column(db.String(20), nullable=False)
	password = db.Column(db.String(128))
	def hash_password(self):
		self.password = generate_password_hash(self.password).decode('utf8')
	def check_password(self, password):
		return check_password_hash(self.password, password)
	
    




@app.route('/')
def hello():   
    return "Hello World!"

@app.route('/movies', methods=['GET'])
def get_movies():
	if request.args.get('genre'):
		movie=Movies.query.filter(Movies.genre.like('%'+request.args.get('genre')+'%')).all()
		print(movie)


		
	
	# movie=Movies.query.all()
	return jsonify({'Movies': Movies.get_all_movies})


# route to get movie by id
@app.route('/movies/<int:id>', methods=['GET'])
def get_movie_by_id(id):
	

    return_value = Movies.get_movie(id)
    return jsonify(return_value)

@app.route('/movies', methods=['POST'])
def add_movie():
    '''Function to add new movie to our database'''
    request_data = request.get_json()  # getting data from client
    Movies.add_movie(request_data["title"], request_data["platform"],
                    request_data["genre"],request_data["editor_choice"],request_data["score"])
    response = Response("Movie addedssssssssss", 201, mimetype='application/json')
    return Response("Movie addsssssssed", 201, mimetype='application/json')

# route to update movie with PUT method
@app.route('/movies/<int:id>', methods=['PUT'])
def update_movie(id):
    '''Function to edit movie in our database using movie id'''
    request_data = request.get_json()
    Movies.update_movie(id, request_data['title'], request_data['platform'],request_data['genre'], request_data['editor_choice'],request_data['score'])
    response = Response("Movie Updated", status=200, mimetype='application/json')
    return response



@app.route('/movies/<int:id>', methods=['DELETE'])
def remove_movie(id):
    '''Function to delete movie from our database'''
    Movies.delete_movie(id)
    response = Response("Movie Deleted", status=200, mimetype='application/json')
    return response
class SignupApi():
 def post(self):
   body = request.get_json()
   user = User(**body)
   user.hash_password()
   user.save()
   id = user.id
   return {'id': str(id)}, 200
class LoginApi():
	def post(self):
		body = request.get_json()
		user = User.objects.get(email=body.get('email'))
		authorized = user.check_password(body.get('password'))
		if not authorized:
			return {'error': 'Email or password invalid'}, 401
		 
		expires = datetime.timedelta(days=7)
		access_token = create_access_token(identity=str(user.id), expires_delta=expires)
		return {'token': access_token}, 200


if __name__ == "__main	__":
  app.run(debug=True)