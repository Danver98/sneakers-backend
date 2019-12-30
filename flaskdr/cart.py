from flask import Blueprint, request , url_for , jsonify , session
from flaskdr.queries import collection_foots
from flaskdr.database import get_db_connection , COLLECTION_NAME
from bson.objectid import ObjectId
import random

from pymongo import MongoClient
from flaskdr.user import User

class Cart:
    __cart = {}
    
    def add_to_cart(self,item_id ,count):
        self.__cart[item_id] = count

    def delete_from_cart(self,item_id):
        self.__cart.pop(item_id)
         
    def clear_cart(self):
        self.__cart.clear()
    # ?
    def update_cart(self,item_id , count):
        for key in self.__cart:
            if key == item_id:
                self.__cart[item_id] = count
                break

    def get_all_items(self):
        return self.__cart


ca = Blueprint('cart',__name__,url_prefix ='/cart')
# Используется 'cart': {'id1':1, 'id2':2 , ...}

def get_new_db_users_col():
    CONNECTION_PASSWORD = "C4pyEOgx7lD1dnce"
    CONNECTION_PASSWORD_PROJECT_2="UJPzENtW2usNKzUj"
    #DATABASE_URI = "mongodb+srv://danver98:{}@cluster0-nsbea.mongodb.net/test?retryWrites=true&w=majority".format(CONNECTION_PASSWORD)
    DATABASE_URI = "mongodb+srv://danver98:{}@cluster1-im2oj.mongodb.net/test?retryWrites=true&w=majority".format(CONNECTION_PASSWORD_PROJECT_2)
    DATABASE = "common_database"
    COLLECTION_NAME = "users_collection"
    con = MongoClient(DATABASE_URI)
    db = con[DATABASE]
    user_col = db[COLLECTION_NAME]
    return user_col

def get_cart_list(email = None):
    user_email = "dicker@mail.ru"
    #user_email = session.get("user").get('email') or request.args.get('email') or email
    #user_col = get_db_connection()[COLLECTION_NAME]
    user_col = get_new_db_users_col()      
    goods = user_col.find_one({"email":user_email}).get("cart")
    if goods is None:
        return None
    cart, total_sum , total_count = [] , 0 ,0
    """
    for i,(k,v) in enumerate(goods.items()):
        item = collection_foots.find_one({"_id":ObjectId(k)}) #?
        cost = item["cost"]
        name = item["name"]
        sum = cost * int(v)
        total_count+=int(v)
        total_sum+=sum
        cart[i] = {"id": k ,"name":name, "cost":cost,"sum":sum}
    return (cart,total_sum , total_count)
    """
    for i,(k,v) in enumerate(goods.items()):
        amount = v
        total_count+=int(v)
        total_sum+=0
        cart.append({"id":k , "amount":int(v)})
    return (cart,total_sum , total_count)
 
@ca.route('/add/', methods = ['GET', 'POST'])
def add_to_cart():
    user_email = "dicker@mail.ru"
    item_id = request.args.get("id")
    item_count = int(request.args.get("count"))
    if (item_id is None) or (item_count is None):
        return( jsonify(error = -2 , messages = "Параметр(ы) не передан(ы)"))
    #user_email = session.get("user")["email"]
    #user_col = get_db_connection()[COLLECTION_NAME]
    user_col = get_new_db_users_col()
    user_col.update_one({"email":user_email} , {"$set": {"cart.{}".format(item_id):item_count}})
    cart = user_col.find_one({"email":user_email}).get("cart")
    return jsonify(error = 0 , cart=cart, messages="Товар добавлен в корзину")

@ca.route('/delete_one/', methods = ['GET', 'DELETE'])
def delete_one_from_cart():
    user_email = "dicker@mail.ru"
    item_id = request.args.get("id")
    if item_id is None:
        return( jsonify(error = -2 , messages = "Параметр 'id товара' не передан"))
    #user_email = session.get("user")["email"]
    #user_col = get_db_connection()[COLLECTION_NAME]
    user_col = get_new_db_users_col()
    user_col.update_one({"email":user_email} , {"$unset": {"cart.{}".format(item_id):""}})
    data = get_cart_list()
    if data is None:
        return jsonify(error = 0 , cart = None ,messages="Корзина пуста")
    return jsonify(error = 0 , cart = data[0] , total_sum = data[1] , total_count = data[2], messages="Товар удалён из корзины")

@ca.route('/delete_all/', methods = ['GET', 'DELETE'])
def delete_all_from_cart():
    user_email = "dicker@mail.ru"
    #user_email = session.get("user").get("email")
    #user_col = get_db_connection()[COLLECTION_NAME]
    user_col = get_new_db_users_col()
    user_col.update_one({"email":user_email} , {"$unset": {"cart":""}})
    return jsonify(error = 0, messages="Корзина очищена")

@ca.route('/update/', methods = ['GET', 'PUT'])
def update_cart():
    pass

@ca.route('/read/', methods = ['GET'])
def read_cart():
    data = get_cart_list()
    if data is None:
        return jsonify(error = 0 , cart = None ,messages="Корзина пуста")
    return jsonify(error = 0 , cart = data[0] , total_sum = data[1] , total_count = data[2], messages="Список товаров корзины")

@ca.route('/in_base/',methods = ['GET'])
def in_base():
    user_col = get_new_db_users_col()
    email = request.args.get('email')
    if email is None:
        return jsonify(error = 1 , messages = "Parameter not specified")
    user = user_col.find_one({"email":email}) 
    if user is None:
        return jsonify(messages = "There is no user with such email")
    cart = user_col.find_one({"email":email}).get("cart")
    return jsonify(cart = cart,messages="testing cart")

@ca.route('/confirm', methods = ['GET', 'POST'])
def receive_confirmation():
    delete_all_from_cart()
    return  jsonify(error = 0 , messages="Ваш заказ {} принят".format(random.randint(000,999)))
    




    