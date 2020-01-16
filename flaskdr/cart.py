from flask import Blueprint, request , url_for , jsonify , session , redirect
from flaskdr.queries import collection_foots
from flaskdr.database import get_db_connection , COLLECTION_NAME
from bson.objectid import ObjectId
import random
from pymongo import MongoClient
from . import queries

class Cart:
    def __init__(self):
        self.__cart = {}
    
    def __call__(self,cart):
        self.__cart = cart

    def add_to_cart(self,item_id ,count):
        self.__cart[item_id] = count

    def delete_from_cart(self,item_id):
        self.__cart.pop(item_id)
         
    def clear_cart(self):
        self.__cart.clear()

    def update_cart(self,item_id , count):
        for key in self.__cart:
            if key == item_id:
                if self.__cart.get(item_id) == None:
                    return None
                self.__cart[key] = count
                break
        return self.__cart

    def get_all_items(self):
        return self.__cart
        
ca = Blueprint('cart',__name__,url_prefix ='/cart')
# Используется 'cart': {'id1':1, 'id2':2 , ...}
# Используется 'cart': {'id1':{'count':1 , 'size':40}, 'id2':{'count':2 , 'size':39}, ...}
def get_cart_raw():  
    user = session.get("user")
    if user is None:
        return session.get("cart")
    else:
        user_col = get_db_connection()[COLLECTION_NAME]
        return user_col.find_one({"email":user["email"]}).get("cart")

def get_cart_list():   
    goods = get_cart_raw()
    if not goods:
        return None
    cart, total_sum , total_count = [] , 0 ,0
    for (k,v) in goods.items():
        item = queries.get_one(k)
        cost = int(item["cost"])
        name = item["name"]
        img = item["img"]
        size = v["size"]
        sum = cost * int(v["count"])
        total_count+=int(v["count"])
        total_sum+=sum
        cart.append({"id": k ,"name":name, "img":img, "size":size, "cost":cost, "count":int(v["count"]), "sum":sum})
    return (cart,total_sum , total_count)      

def reset_db_goods_count(item_id = None):
    goods = get_cart_raw()
    if not goods:
        return
    if item_id is not None:
        item = queries.get_one(item_id)
        item["count"]+=goods.get(item_id).get("count")
        return
    for (k,v) in goods.items():
        item = queries.get_one(k)
        item["count"]+=v["count"]

def make_count_and_size(item_id):
    sizes = queries.get_one(item_id)["size"]
    if len(sizes) == 0:
        size = None
    else:
        size = sizes[0]
    item = {"count":1 , "size":size}
    return item

def add_to_session_cart(item_id):
    if session.get("cart") is None:
        session["cart"] = {}
    #queries.update_count(item_id, -1)
    session["cart"][item_id] = make_count_and_size(item_id)
    session.modified = True
    return session["cart"]

def add_to_user_cart(user_email,item_id):
    user_col = get_db_connection()[COLLECTION_NAME]
    #queries.update_count(item_id, -1)   
    user_col.update_one({"email":user_email} , {"$set": {"cart.{}".format(item_id):make_count_and_size(item_id)}})  
    return user_col.find_one({"email":user_email}).get("cart")
    
def change_session_cart(item_id , key , value):
    #if key == "count" :
        #before = session["cart"].get(item_id).get("count",0)
        #queries.update_count(item_id, before - int(count))
    session["cart"][item_id][key] = value
    session.modified = True
    return session["cart"]

def change_user_cart(user_email,item_id,key,value):
    user_col = get_db_connection()[COLLECTION_NAME]
    #if key == "count" in kwargs:
        #before = user_col.find_one({"email":user_email}).get("cart").get(item_id).get(count,0)
        #queries.update_count(item_id, before - int(count))
    user_col.update_one({"email":user_email} , {"$set": {"cart.{}.{}".format(item_id,key):value}})  
    return user_col.find_one({"email":user_email}).get("cart")

def del_from_session_cart(item_id = None):
    if session.get("cart") is None:
        return
    if item_id is not None:
        #reset_db_goods_count(item_id)
        session["cart"].pop(item_id,None)       
    else:
        #reset_db_goods_count()
        session["cart"].clear()
    session.modified = True

def del_from_user_cart(user_email,item_id = None):
    user_col = get_db_connection()[COLLECTION_NAME]
    if item_id is not None:
        #reset_db_goods_count(item_id)
        user_col.update_one({"email":user_email} , {"$unset": {"cart.{}".format(item_id):""}})    
    else:
        #reset_db_goods_count()
        user_col.update_one({"email":user_email} , {"$unset": {"cart":""}})
"""
def update_it(data, key ):  
    item_id = data.get("_id") or request.args.get("id")
    value = data.get(key) or request.args.get(key)
    if (item_id is None) or (value is None):
        return( jsonify(error = -1 , messages = "Параметр(ы) не передан(ы)"))
    problem = check(item_id , key , value)
    if problem is not None:
        return jsonify(error = problem[0] , messages = problem[1])
    user = session.get("user")
    if user is None:
        change_session_cart(item_id,key,value)
    else:
        change_user_cart(user["email"],item_id,key,value)
    return jsonify(error = 0, messages="Товар обновлён")       

def check_count(item_id , count):
    good = queries.get_one(item_id)
    if good.get("count") < (count - good_count["count"]):
        return (-3, "Такого количества товара нет на складе")
    return None 

def check(item_id , param , value):
    goods = get_cart_raw()
    if not goods:
        return (0, "Корзина пуста")   
    good_count = goods.get(item_id)
    if good_count is None:
        return (-2, "Товара с данным id нет в корзине")
    if param == "count":
        return check_count(item_id , value)
    else:
        return check_size(item_id , value)
"""
def check_item(item_id , count):
    goods = get_cart_raw()
    if not goods:
        return (0, "Корзина пуста")   
    good_count = goods.get(item_id)
    if good_count is None:
        return (-2, "Товара с данным id нет в корзине")
    good = queries.get_one(item_id)
    if good.get("count") < (count - good_count["count"]):
        return (-3, "Такого количества товара нет на складе")
    return None  
 
def check_size(item_id, size):
    goods = get_cart_raw()
    if not goods:
        return (0, "Корзина пуста")
    good = queries.get_one(item_id)
    if (size not in good.get("size")):
        return (-4, "Товара с данным размером нет на складе")
    return None

@ca.route('/add/', methods = ['POST'])
def add_to_cart():
    data = request.get_json(silent = True)
    item_id = data.get("_id") or request.args.get("id")
    if item_id is None:
        return( jsonify(error = -2 , messages = "Параметр(ы) не передан(ы)"))
    if queries.get_one(item_id).get("count") <= 0:
        return( jsonify(error = -3 , messages = "Товар отсутствует на складе"))
    user = session.get("user")
    if user is None:
        add_to_session_cart(item_id)
    else:
        add_to_user_cart(user["email"] , item_id)
    return jsonify(error = 0 , messages="Товар добавлен в корзину")

@ca.route('/delete_one/', methods = ['POST', 'DELETE'])
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

@ca.route('/update/', methods = ['PUT' , 'POST'])
def update_cart():
    cart = get_cart_raw()
    if cart is None:
        return jsonify(error = 0 , cart = None ,messages="Корзина пуста")
    data = request.get_json(silent = True)
    item_id = data.get("_id") or request.args.get("id")
    count = data.get("count") or request.args.get("count")
    if (item_id is None) or (count is None):
        return( jsonify(error = -1 , messages = "Параметр(ы) не передан(ы)"))
    problem = check_item(item_id , count)
    if problem is not None:
        return jsonify(error = problem[0] , messages = problem[1])
    user = session.get("user")
    if user is None:
        change_session_cart(item_id,"count" ,int(count))
    else:
        change_user_cart(user["email"],item_id,"count" ,int(count))
    return jsonify(error = 0, messages="Товар обновлён")
    #data = get_cart_list()
    #return jsonify(error = 0 , cart = data[0] , total_sum = data[1] , total_count = data[2], messages="Товар обновлён")

@ca.route('/update_size/', methods = ['PUT' , 'POST'])
def update_size():
    cart = get_cart_raw()
    if cart is None:
        return jsonify(error = 0 , cart = None ,messages="Корзина пуста")
    data = request.get_json(silent = True)
    item_id = data.get("_id") or request.args.get("id")
    size = data.get("size") or request.args.get("size")
    if (item_id is None) or (size is None):
        return( jsonify(error = -1 , messages = "Параметр(ы) не передан(ы)"))
    problem = check_size(item_id, float(size))
    if problem is not None:
        return jsonify(error = problem[0] , messages = problem[1])
    user = session.get("user")
    if user is None:
        change_session_cart(item_id,"size",float(size))
    else:
        change_user_cart(user["email"],item_id,"size",float(size))
    return jsonify(error = 0, messages="Товар обновлён")    
    #data = get_cart_list()
    #return jsonify(error = 0 , cart = data[0] , total_sum = data[1] , total_count = data[2], messages="Товар обновлён") 

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
        return("From cart/test_for_logged(): user is authorized: " + str(user))
    
@ca.route('/confirm', methods = ['GET', 'POST'])
def receive_confirmation():
<<<<<<< HEAD
     # собираю инфу с корзины и передаю в новую колекцию
     
=======
>>>>>>> e510992b6152e62382a6c58006c3d323f256c275
    delete_all_from_cart()
    return  jsonify(error = 0 , messages="Ваш заказ {} принят".format(random.randint(000,999)))
    




    
