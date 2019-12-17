from flask import request , g ,flash, url_for, session , redirect ,current_app , Blueprint , render_template , get_flashed_messages , jsonify
from datetime import datetime , date
from werkzeug.security import check_password_hash, generate_password_hash
from bson import json_util
import functools,json
bp = Blueprint('auth',__name__,url_prefix ='/auth')

@bp.route('/register/', methods = ['GET','POST'])
def register():
    credentials = {}
    if request.method == 'POST':
        data = request.get_json(force = True)
        first_name =data['firstName']
        last_name = data['lastName'] 
        password = data['password'] 
        phone = data['telephone']
        email = data['email'] 
        birth_date = data['birthday']
        credentials = data.to_dict().pop("password")
        error = None
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
            from . import database
            from . import user  
            user = user.User(first_name,last_name,birth_date,phone,email,password)
            col = database.get_db_connection()[database.COLLECTION_NAME]
            if col.find_one({"email": email}) is None:
                col.insert(user.get_user_data())
                flash("Вы успешно зарегистрировались!")
                return jsonify(registered = True ,credentials = credentials, messages = get_flashed_messages())
            else:
                flash("Пользователь с данным e-mail уже существует")
    return jsonify(registered = False ,credentials = credentials, messages = get_flashed_messages())


@bp.route('/login/',methods = ['GET','POST'])
def login():
    credentials = {}
    if request.method == 'POST':
        data = request.get_json(force = True)
        print("========")
        print(data)
        print("========")
        email = data['email']
        password = data['password']
        credentials = data.to_dict().pop("password")
        error = None
        if not email:
            error = "Не указан e-mail"
            flash(error)
        if not password:
           error = "Не указан пароль"
           flash(error)
        if error is None:
            from . import database
            from . import user 
            col = database.get_db_connection()[database.COLLECTION_NAME]
            doc = col.find_one({"email":email})
            if doc is None:
                error = "Неверный логин/почта"
                flash(error)
            elif check_password_hash(doc['password'],password):
                user = user.User.convert_from_doc(doc)
                session.clear()
                session['user'] = user.get_user_data().pop("password")
                session['user_id'] = str(doc['_id'])
                flash("Вы успешно вошли!")
                return  jsonify(logged = True , credentials = session['user'] , messages = get_flashed_messages())
            else:
                error = "Неверный пароль"
                flash(error)
    return jsonify( logged = False, credentials = credentials , messages = get_flashed_messages()) 
    
@bp.route('/logout/', methods=['POST', 'GET'])
def logout():
    session.clear()
    return jsonify(logged_out = True)


@bp.before_app_request
def initalize_logged_user():
    user = None
    user = session.get('user')
    if user is None:
        g.user = None
    else:
        g.user = user
        g.user_id = session.get('user_id')
    

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return jsonify(login_required = True)
        return view(**kwargs)
    return wrapped_view



