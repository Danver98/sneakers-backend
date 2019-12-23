from flask import Flask , request , render_template , Response , jsonify
from flask_cors import CORS
from instance.config import *
from flaskdr.custom_response import CustomResponse
from pymongo.errors import ConnectionFailure
from werkzeug.exceptions import HTTPException, InternalServerError
import pymongo, os
SECRET_KEY = "*F-JaNdRgUkXp2s5v8y/B?E(H+KbPeSh"
CONNECTION_PASSWORD = "C4pyEOgx7lD1dnce"
ADMIN_NAME = " "
DATABASE_URI = "mongodb+srv://danver98:{}@cluster0-nsbea.mongodb.net/test?retryWrites=true&w=majority".format(CONNECTION_PASSWORD)

# добавить @login_required для других страниц

def create_app(test_config = None,debug_config = True ,instance_relative_config = False):
    app = Flask(__name__)
    app.response_class = CustomResponse
    if debug_config:
        app.config.from_mapping(
            SECRET_KEY = SECRET_KEY,
            DATABASE_URI = DATABASE_URI
        )
    else:
        app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY") or SECRET_KEY
        app.config.from_pyfile('production-config.py')
    CORS(app)
    #app.config.from_object(Configuration())
    from . import database
    # если @app.teardown_appcontext не используется
    database.init_db(app)
    from . import auth
    app.register_blueprint(auth.bp)

    from . import catalog
    app.register_blueprint(catalog.app_catalog)
    
    from . import cart
    app.register_blueprint(cart.ca)

    @app.route('/')
    def main_page():
        return jsonify(success = True,messages="This is app main page") 
    
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        if isinstance(e,InternalServerError):
            return jsonify(error = -1 , messages = "Упс,произошла ошибка на сервере. Попробуйте выполнить действие ещё раз")
        return jsonify(error = -2 , messages = "Упс,произошла ошибка при передаче данных. Попробуйте ещё раз")
       
    @app.errorhandler(ConnectionFailure)
    def database_exception(e):
        jsonify(error = -3 , messages = "Не удаётся выполнить запрос к базе данных. Попробуйте ещё раз")
     
    return app

