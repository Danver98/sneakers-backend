from flask import Blueprint, request , url_for , jsonify , session , redirect
from flaskdr.queries import collection_foots
from flaskdr.database import get_db_connection , COLLECTION_NAME
from bson.objectid import ObjectId
import random
from pymongo import MongoClient
from . import queries

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
                if self.__cart.get(item_id) == None:
                    return None
                self.__cart[item_id] = count
                break
        return self.__cart

    def get_all_items(self):
        return self.__cart
        
ca = Blueprint('cart',__name__,url_prefix ='/cart')
# Используется 'cart': {'id1':1, 'id2':2 , ...}
#user_col.update_one({"email":user_email} , {"$unset": {"cart.{}".format(item_id):""}}) - del one
#user_col.update_one({"email":user_email} , {"$unset": {"cart":""}}) - clear
#user_col.update_one({"email":user_email} , {"$set": {"cart.{}".format(item_id):count}}) - add
#user_col.update_one({"email":user_email} , {"$set": {"cart.{}".format(item_id):int(item_count)}}) - update

def change_session_cart(item_id, count):
    if session.get("cart") is None:
        session["cart"] = {}
    #queries.update_count(item_id, -amount)
    session["cart"][item_id] = int(count)
    session.modified = True
    return session["cart"]
    
def change_user_cart(user_email,item_id,count):
    user_col = get_db_connection()[COLLECTION_NAME]
    #before = user_col.find_one({"email":user_email}).get("cart")[item_id]
    user_col.update_one({"email":user_email} , {"$set": {"cart.{}".format(item_id):int(count)}})
    #queries.update_param(item_id,"count",before - count)
    return user_col.find_one({"email":user_email}).get("cart")

def del_from_session_cart(item_id = None):
    if session.get("cart") is None:
        return
    if item_id is not None:
        session["cart"].pop(item_id)
        #queries.update_count(item_id, +amount)
    else:
        session["cart"].clear()
        #queries.update_all()
    session.modified = True

def del_from_user_cart(user_email,item_id = None):
    user_col = get_db_connection()[COLLECTION_NAME]
    if item_id is not None:
        user_col.update_one({"email":user_email} , {"$unset": {"cart.{}".format(item_id):""}})
        #queries.update_count(item_id, +amount)
    else:
        user_col.update_one({"email":user_email} , {"$unset": {"cart":""}})
        #queries.update_all()

def get_new_db_users_col():
    CONNECTION_PASSWORD_PROJECT_2="UJPzENtW2usNKzUj"
    DATABASE_URI = "mongodb+srv://danver98:{}@cluster1-im2oj.mongodb.net/test?retryWrites=true&w=majority".format(CONNECTION_PASSWORD_PROJECT_2)
    DATABASE = "common_database"
    COLLECTION_NAME = "users_collection"
    con = MongoClient(DATABASE_URI)
    db = con[DATABASE]
    user_col = db[COLLECTION_NAME]
    return user_col

def get_cart_list():   
    user = session.get("user")
    if user is None:
        goods = session.get("cart")
    else:
        user_col = get_db_connection()[COLLECTION_NAME]
        goods = user_col.find_one({"email":user["email"]}).get("cart")
    if not goods:
        return None
    cart, total_sum , total_count = [] , 0 ,0
    for i,(k,v) in enumerate(goods.items()):
        item = queries.get_one(k)
        cost = item["cost"]
        name = item["name"]
        sum = cost * int(v)
        total_count+=int(v)
        total_sum+=sum
        cart.append({"id": k ,"name":name, "cost":cost,"sum":sum})
    return (cart,total_sum , total_count)
      
@ca.route('/add/', methods = ['GET', 'POST'])
def add_to_cart():
    error = None
    if request.method == 'GET':
        return jsonify(error = error , messages = "That was GET method")
    data = request.get_json(silent = True)
    item_id = data.get("_id") or request.args.get("id")
    if item_id is None:
        return( jsonify(error = -2 , messages = "Параметр(ы) не передан(ы)"))
    if queries.get_one(item_id).get("count") <= 0:
        return( jsonify(error = -3 , messages = "Товар отсутствует на складе"))
    user = session.get("user")
    if user is None:
        cart = change_session_cart(item_id,1)
    else:
        cart = change_user_cart(user["email"] , item_id, 1)
    return jsonify(error = 0 , cart=cart, messages="Товар добавлен в корзину")

@ca.route('/delete_one/', methods = ['GET', 'DELETE'])
def delete_one_from_cart():
    data = request.get_json(silent = True)
    item_id = data.get("_id") or request.args.get("id")
    if item_id is None:
        return( jsonify(error = -2 , messages = "Параметр 'id товара' не передан"))
    user = session.get("user")
    if user is None:
        del_from_session_cart(item_id)
    else:
        del_from_user_cart(user["email"],item_id)   
    data = get_cart_list()
    if data is None:
        return jsonify(error = 0 , cart = None ,messages="Корзина пуста")
    return jsonify(error = 0 , cart = data[0] , total_sum = data[1] , total_count = data[2], messages="Товар удалён из корзины")

@ca.route('/delete_all/', methods = ['GET', 'DELETE' , 'POST'])
def delete_all_from_cart():
    user = session.get("user")
    if user is None:
        del_from_session_cart()
    else:
        del_from_user_cart(user["email"])
    return jsonify(error = 0, messages="Корзина очищена")

@ca.route('/update/', methods = ['GET', 'PUT' , 'POST'])
def update_cart():
    data = get_cart_list()
    if data is None:
        return jsonify(error = 0 , cart = None ,messages="Корзина пуста")
    data = request.get_json(silent = True)
    item_id = data.get("_id") or request.args.get("id")
    count = data.get("count") or request.args.get("count")
    if (item_id is None) or (count is None):
        return( jsonify(error = -2 , messages = "Параметр(ы) не передан(ы)"))
    #if queries.get_one(item_id).get("count") < count:
    #return( jsonify(error = -3 , messages = "Такого количества товара нет на складе"))
    user = session.get("user")
    if user is None:
        good = session.get("cart").get(item_id)
        if good is None:
            return( jsonify(error = -1 , messages = "Товара с данным id нет в корзине")) 
        change_session_cart(item_id,count)
    else:
        user_email = session.get("user")["email"]
        user_col = get_db_connection()[COLLECTION_NAME]
        good = user_col.find_one({"$and":[{"email":user_email} , {"cart.$":{"$eq":item_id}}]})
        if good is None:
            return( jsonify(error = -1 , messages = "Товара с данным id нет в корзине")) 
        change_user_cart(user_email,item_id,count)
    data = get_cart_list()
    return jsonify(error = 0 , cart = data[0] , total_sum = data[1] , total_count = data[2], messages="Товар удалён из корзины")

@ca.route('/read/', methods = ['GET'])
def read_cart():
    data = get_cart_list()
    if data is None:
        return jsonify(error = 0 , cart = None ,messages="Корзина пуста")
    return jsonify(error = 0 , cart = data[0] , total_sum = data[1] , total_count = data[2], messages="Список товаров корзины")

@ca.route('/test/', methods = ['GET','POST'])
def test_for_logged():
    user = session.get("user")
    if not user:
        return("From cart/test_for_logged(): user is not authorized!")
    else:
        return("From cart/test_for_logged(): user is authorized: " + user)

@ca.route('/confirm', methods = ['GET', 'POST'])
def receive_confirmation():
    delete_all_from_cart()
    return  jsonify(error = 0 , messages="Ваш заказ {} принят".format(random.randint(000,999)))
    




    
