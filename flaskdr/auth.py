from flask import request , g ,flash, url_for, session , redirect ,current_app , Blueprint , render_template , get_flashed_messages , jsonify
from datetime import datetime , date
from werkzeug.security import check_password_hash, generate_password_hash
from bson import json_util
import functools,json,os
from . import database 
from flaskdr.user import User 
bp = Blueprint('auth',__name__,url_prefix ='/auth')

@bp.route('/register/', methods = ['POST'])
def register():
    data = request.get_json(force = True) 
    first_name = data.get('firstName')
    last_name = data.get('lastName') 
    password = data.get('password') 
    phone = "+7" + data.get('telephone')
    email = data.get('email') 
    birth_date = data.get('birthday')
    error = None
    if not first_name:
        error = "Не указано имя"
        flash(error)
    if not last_name:
        error = "Не указана фамилия"
        flash(error)
    if not data.get('telephone'):
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
            #session.clear()
            session.pop("user",None)
            session['user'] = user.get_user_data_no_passwd()
            if session.get("cart") is not None:
                col.update_one({"email":email} ,{"$set": {"cart":session.get("cart")}})
            return jsonify(error = 0, messages = get_flashed_messages())
        else:
            error = 1
            flash("Пользователь с данным e-mail уже существует")
    return jsonify(error = error, messages = get_flashed_messages())

@bp.route('/login/',methods = ['POST'])
def login():
    data = request.get_json(force = True)
    email = data.get('email')
    password = data.get('password')
    error = None
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
            #session.clear()
            session.pop("user",None)
            #session.pop("user_id",None)
            session['user'] = user.get_user_data_no_passwd()
            print("From login() - The user is:"+ str(session.get("user")))
            #session['user_id'] = str(doc['_id'])
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
    print("From logout() - The user is: " + str(session.get("user")))
    session.clear()
    return jsonify(error = 0, messages = "Пользователь вышел из аккаунта")

@bp.route('/test/', methods = ['GET','POST'])
def test_for_logged():
    user = session.get("user")
    if not user:
        return("From auth/test_for_logged(): user is not authorized!")
    else:
        return("From auth/test_for_logged(): user is authorized: " + str(user))

@bp.before_app_request
def initalize_logged_user():
    user = session.get('user')
    if user is None:
        g.user = None
        print("From initalize_logged_user() - the user is unauthorized!: ")
    else:
        print("From initalize_logged_user() - the user is authorized!: " + str(user))
        g.user = user
        #g.user_id = session.get('user_id')
        #g.user_email = session.get('user').get('email)
    
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            error = 3
            return jsonify( error = error, message = "Необходима авторизация")
        return view(**kwargs)
    return wrapped_view



