from flask import request , g ,flash, url_for, session , redirect ,current_app , Blueprint , render_template , get_flashed_messages , jsonify
from datetime import datetime , date
from werkzeug.security import check_password_hash, generate_password_hash
from bson import json_util
import functools,json
from . import database 
from flaskdr.user import User 
bp = Blueprint('auth',__name__,url_prefix ='/auth')

@bp.route('/register/', methods = ['GET','POST'])
def register():
    error = None
    if request.method == 'GET':
        return jsonify(error = error , messages = "That was GET method")
    data = request.get_json(force = True)
    first_name = data['firstName']
    last_name = data['lastName'] 
    password = data['password'] 
    phone = "+7" + data['telephone']
    email = data['email'] 
    birth_date = data['birthday']
    if not first_name:
        error = "Не указано имя"
        flash(error)
    if not last_name:
        error = "Не указана фамилия"
        flash(error)
    if not phone:
        error = "Не указан телефон"
        flash(error)
    if not email:
        error = "Не указан e-mail"
        flash(error)
    if not birth_date:
        error = "Не указана дата рождения"
        flash(error)  
    if not password:
        error = "Не указан пароль"
        flash(error)
    if error is None: 
        user = User(first_name,last_name,birth_date,phone,email,password)
        col = database.get_db_connection()[database.COLLECTION_NAME]
        if col.find_one({"email": email}) is None:
            col.insert(user.get_user_data())
            flash("Вы успешно зарегистрировались!")
            return jsonify(error = 0, messages = get_flashed_messages())
        else:
            error = 1
            flash("Пользователь с данным e-mail уже существует")
    return jsonify(error = error, messages = get_flashed_messages())

@bp.route('/login/',methods = ['GET','POST'])
def login():
    error = None
    if request.method == 'GET':
        return jsonify(error = error , messages = "That was GET method")
    data = request.get_json(force = True)
    email = data['email']
    password = data['password']
    if not email:
        error = "Не указан e-mail"
        flash(error)
    if not password:
        error = "Не указан пароль"
        flash(error)
    if error is None:
        col = database.get_db_connection()[database.COLLECTION_NAME]
        doc = col.find_one({"email":email})
        if doc is None:
            error = 1
            flash("Не существует пользователя с таким логином(почтой)")
        elif check_password_hash(doc['password'],password):
            user = User.convert_from_doc(doc)
            session.clear()
            session['user'] = user.get_user_data_no_passwd()
            print("From login() - The user is:"+ session.get("user"))
            session['user_id'] = str(doc['_id'])
            if session.get("cart") is not None:
                col.update_one({"email":email} ,{"$set": {"cart":session.get("cart")}})
            credentials = {"firstName": user.first_name , "lastName": user.last_name}
            flash("Вы успешно вошли!")
            return  jsonify( error = 0, credentials = credentials , messages = get_flashed_messages())
        else:
            error = 2
            flash("Неверный пароль")
    return jsonify(error = error , messages = get_flashed_messages()) 
    
@bp.route('/logout/', methods=['GET' ,'POST'])
def logout():
    print("From logout() - The user is: " + session.get("user"))
    session.clear()
    print("=====")
    print("LOGOUT MESSAGE")
    print("=====")
    return jsonify(error = 0, messages = "Пользователь вышел из аккаунта")

@bp.route('/test/', methods = ['GET','POST'])
def test_for_logged():
    user = session.get("user")
    if not user:
        return("From auth/test_for_logged(): user is not authorized!")
    else:
        return("From auth/test_for_logged(): user is authorized: " + user)

@bp.before_app_request
def initalize_logged_user():
    user = session.get('user')
    if user is None:
        g.user = None
    else:
        print("User is authorized!: " + user)
        g.user = user
        g.user_id = session.get('user_id')
        #g.user_email = session.get('user').get('email)
    
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            error = 3
            return jsonify( error = error, message = "Необходима авторизация")
        return view(**kwargs)
    return wrapped_view



