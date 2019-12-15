from flask import Flask , request , render_template , Response , jsonify
from flask_cors import CORS
from instance.config import *
from flaskdr.custom_response import CustomResponse
from pymongo.errors import ConnectionFailure
from werkzeug.exceptions import HTTPException
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
    @app.route('/')
    def main_page():
        print("Starting the app...")
        return jsonify(returned = True , message="Tryna to start Heroku")
        #return render_template('index.html')
    
    @app.errorhandler(HTTPException)
    def handle_exception(e):    
        return jsonify(success = False , code = e.code, name = e.name,description = e.description)
        
    @app.errorhandler(ConnectionFailure)
    def database_exception(e):
        response = e.get_response()
        jsonify(success = False , code = 500 , name = "database" , description = "cannot complete request to database")
        
    return app

