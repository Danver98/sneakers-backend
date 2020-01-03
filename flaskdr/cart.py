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
                self.__cart[item_id] = count
                break

    def get_all_items(self):
        return self.__cart


ca = Blueprint('cart',__name__,url_prefix ='/cart')
# Используется 'cart': {'id1':1, 'id2':2 , ...}
#user_email = "dicker@mail.ru"

def get_new_db_users_col():
    CONNECTION_PASSWORD_PROJECT_2="UJPzENtW2usNKzUj"
    DATABASE_URI = "mongodb+srv://danver98:{}@cluster1-im2oj.mongodb.net/test?retryWrites=true&w=majority".format(CONNECTION_PASSWORD_PROJECT_2)
    DATABASE = "common_database"
    COLLECTION_NAME = "users_collection"
    con = MongoClient(DATABASE_URI)
    db = con[DATABASE]
    user_col = db[COLLECTION_NAME]
    return user_col

def get_cart_list(email = None):
    user_email = session.get("user")["email"] or request.args.get('email') or email
    user_col = get_db_connection()[COLLECTION_NAME]
    #user_col = get_new_db_users_col()  # comment for heroku    
    goods = user_col.find_one({"email":user_email}).get("cart")
    if goods is None:
        return None
    cart, total_sum , total_count = [] , 0 ,0
    """
    for i,(k,v) in enumerate(goods.items()): # comment for heroku
        amount = v
        total_count+=int(v)
        total_sum+=0
        cart.append({"id":k , "amount":int(v)})
    return (cart,total_sum , total_count)
    """
    for i,(k,v) in enumerate(goods.items()):
        item = collection_foots.find_one({"_id":ObjectId(k)}) #?
        cost = item["cost"]
        name = item["name"]
        sum = cost * int(v)
        total_count+=int(v)
        total_sum+=sum
        cart.append({"id": k ,"name":name, "cost":cost,"sum":sum})
    return (cart,total_sum , total_count)
    
   
@ca.route('/add/', methods = ['GET', 'POST'])
def add_to_cart():
    #data = request.get_json() - если будет POST + возврат, если GET
    item_id = request.args.get("id") # or data['id'] - POST
    if item_id is None:
        return( jsonify(error = -2 , messages = "Параметр(ы) не передан(ы)"))
    if queries.get_one(item_id).get("count") <= 0:
        return( jsonify(error = -3 , messages = "Товар отсутствует на складе/нет такого количества")) 
    user_email = session.get("user")["email"]
    user_col = get_db_connection()[COLLECTION_NAME]
    #user_col = get_new_db_users_col() # comment for heroku
    #queries.update_count(item_id, - 1)
    user_col.update_one({"email":user_email} , {"$set": {"cart.{}".format(item_id):1}})
    cart = user_col.find_one({"email":user_email}).get("cart")
    return jsonify(error = 0 , cart=cart, messages="Товар добавлен в корзину")

@ca.route('/delete_one/', methods = ['GET', 'DELETE'])
def delete_one_from_cart():
    #data = request.get_json() - если будет DELETE/POST + возврат, если GET
    item_id = request.args.get("id") # or data['id'] - POST/DELETE
    if item_id is None:
        return( jsonify(error = -2 , messages = "Параметр 'id товара' не передан"))
    user_email = session.get("user")["email"]
    user_col = get_db_connection()[COLLECTION_NAME]
    #user_col = get_new_db_users_col() # comment for heroku
    user_col.update_one({"email":user_email} , {"$unset": {"cart.{}".format(item_id):""}})
    data = get_cart_list()
    if data is None:
        return jsonify(error = 0 , cart = None ,messages="Корзина пуста")
    return jsonify(error = 0 , cart = data[0] , total_sum = data[1] , total_count = data[2], messages="Товар удалён из корзины")

@ca.route('/delete_all/', methods = ['GET', 'DELETE' , 'POST'])
def delete_all_from_cart():
    user_email = session.get("user").get("email")
    user_col = get_db_connection()[COLLECTION_NAME]
    #user_col = get_new_db_users_col() # comment for heroku
    user_col.update_one({"email":user_email} , {"$unset": {"cart":""}})
    return jsonify(error = 0, messages="Корзина очищена")

@ca.route('/update/', methods = ['GET', 'PUT' , 'POST'])
def update_cart():
    data = get_cart_list()
    if data is None:
        return jsonify(error = 0 , cart = None ,messages="Корзина пуста")
    #data = request.get_json() - если будет POST + возврат, если GET
    item_id = request.args.get("id") # or data['id'] - POST
    item_count = request.args.get("count") # or data['count'] - POST
    if (item_id is None) or (item_count is None):
        return( jsonify(error = -2 , messages = "Параметр(ы) не передан(ы)"))
    user_email = session.get("user")["email"]
    user_col = get_db_connection()[COLLECTION_NAME]
    #user_col = get_new_db_users_col() # comment for heroku
    good = user_col.find_one({"$and":[{"email":user_email} , {"cart.$":{"$eq":item_id}}]})
    if good is None:
        return( jsonify(error = -1 , messages = "Товара с данным id нет в корзине"))
    #if queries.get_one(item_id).get("count") < item_count:
        #return( jsonify(error = -3 , messages = "Такого количества товара нет на складе")) 
    #before = user_col.find_one({"email":user_email}).get("cart")[item_id]
    #queries.update_param(item_id,"count",before - item_count)
    user_col.update_one({"email":user_email} , {"$set": {"cart.{}".format(item_id):int(item_count)}})
    data = get_cart_list()
    return jsonify(error = 0 , cart = data[0] , total_sum = data[1] , total_count = data[2], messages="Товар удалён из корзины")

@ca.route('/read/', methods = ['GET'])
def read_cart():
    data = get_cart_list()
    if data is None:
        return jsonify(error = 0 , cart = None ,messages="Корзина пуста")
    return jsonify(error = 0 , cart = data[0] , total_sum = data[1] , total_count = data[2], messages="Список товаров корзины")

@ca.route('/confirm', methods = ['GET', 'POST'])
def receive_confirmation():
    delete_all_from_cart()
    return  jsonify(error = 0 , messages="Ваш заказ {} принят".format(random.randint(000,999)))
    




    