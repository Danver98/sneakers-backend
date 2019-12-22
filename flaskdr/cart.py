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


from flask import Blueprint, request , url_for , jsonify , session
from flaskdr.queries import collection_foots
from flaskdr.database import get_db_connection , COLLECTION_NAME

ca = Blueprint('cart',__name__,url_prefix ='/cart')

# Используется 'cart': {'id1':1, 'id2':2 , ...}
 
@ca.route('/add/', methods = ['GET', 'POST'])
def add_to_cart():
    item_id = request.args.get("id")
    item_count = int(request.args.get("count"))
    if (item_id is None) or (item_count is None):
        return( jsonify(error = -2 , messages = "Параметр(ы) не передан(ы)"))
    user_email = session.get("user")["email"]
    user_col = get_db_connection()[COLLECTION_NAME]
    user_col.update({"email":user_email} , {"$set": {"cart.{}".format(item_id):item_count}})
    return jsonify(error = 0 , messages="Товар добавлен в корзину")

@ca.route('/delete/', methods = ['GET', 'POST'])
def delete_from_cart():
    item_id = request.args.get("id")
    if item_id is None:
        return( jsonify(error = -2 , messages = "Параметр 'id товара' не передан"))
    user_email = session.get("user")["email"]
    user_col = get_db_connection()[COLLECTION_NAME]
    user_col.update({"email":user_email} , {"$unset": {"cart.{}".format(item_id):""}})
    return jsonify(error = 0 , messages="Товар удалён из корзины")

@ca.route('/update/', methods = ['GET', 'POST'])
def update_cart():
    pass

@ca.route('/read/', methods = ['GET' , 'POST'])
def read_cart():
    user_email = session.get("user")["email"]
    user_col = get_db_connection()[COLLECTION_NAME]
    goods = user_col.find({"email":user_email})["cart"]
    cart = []
    for i,(k,v) in enumerate(goods.items()):
        cost = collection_foots.find_one({"_id":k})["cost"]
        total_price = cost * int(v)
        cart[i] = {"id": k ,"cost":cost,"total_price":total_price}   
    return jsonify(error = 0 , cart = cart , messages="Список товаров корзины")




#передать Жене
@ca.route('/confirm', methods = ['GET', 'POST'])
def some_to_do():
    pass




    