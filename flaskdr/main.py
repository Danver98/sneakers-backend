from flask import Flask , request , render_template , Response , jsonify , session
from flask_cors import CORS
from instance.config import *
from flaskdr.custom_response import CustomResponse
from pymongo.errors import ConnectionFailure
from werkzeug.exceptions import HTTPException, InternalServerError
from . import  auth, catalog , cart , database
import pymongo, os , traceback , datetime , redis
SECRET_KEY = "*F-JaNdRgUkXp2s5v8y/B?E(H+KbPeSh"
CONNECTION_PASSWORD_PROJECT_2="UJPzENtW2usNKzUj"
DATABASE_URI = "mongodb+srv://danver98:{}@cluster1-im2oj.mongodb.net/test?retryWrites=true&w=majority".format(CONNECTION_PASSWORD_PROJECT_2)

def create_app(instance_relative_config = False):
    app = Flask(__name__)
    app.response_class = CustomResponse
    app.config.from_mapping(
        SECRET_KEY = os.environ.get("SECRET_KEY") or SECRET_KEY,
        DATABASE_URI = DATABASE_URI
    )
    CORS(app, supports_credentials = True)
    #app.config.from_object(Configuration())
    # если @app.teardown_appcontext не используется
    database.init_db(app)   
    app.register_blueprint(auth.bp)   
    app.register_blueprint(catalog.app_catalog)
    app.register_blueprint(cart.ca)

    @app.route('/')
    def main_page():
        return jsonify(success = True,messages="This is app main page") 
    
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        if isinstance(e,InternalServerError):
            print(traceback.format_exc())
            return jsonify(error = -1 , messages = "Упс,произошла ошибка на сервере. Попробуйте выполнить действие ещё раз")
        return jsonify(error = -2 , messages = "Упс,произошла ошибка при передаче данных. Попробуйте ещё раз")
       
    @app.errorhandler(ConnectionFailure)
    def database_exception(e):
        print(traceback.format_exc())
        jsonify(error = -3 , messages = "Не удаётся выполнить запрос к базе данных. Попробуйте ещё раз")
    
    return app