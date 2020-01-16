from datetime import datetime , date
from flaskdr.cart import Cart
from werkzeug.security import check_password_hash, generate_password_hash
import pymongo
class User(object):
    def __init__(self,first_name,last_name,birth_date,phone, email,password , cart = None):
        self.__first_name = first_name
        self.__last_name = last_name
        if isinstance(birth_date,str):        
            self.__birth_date = datetime.strptime(birth_date,"%Y-%m-%d")
        else:
            self.__birth_date = birth_date
        self.__phone = phone
        self.__email = email
        self.__password = generate_password_hash(password)
        if cart is None:
            self.__cart = Cart()
        else:
            self.__cart = cart

    def _set_date(self,birth_date):
        if isinstance(birth_date, date):
            return birth_date     
        elems = birth_date.split("-")
        if len(elems) != 3:
            raise Exception
        return date(int(elems[0]) , int(elems[1]) , int(elems[2]))

    @property
    def first_name(self):
        return self.__first_name

    @property
    def last_name(self):
        return self.__last_name

    @property
    def birth_date(self):
        return self.__birth_date
    
    @property
    def phone(self):
        return self.__phone
    
    @property
    def email(self):
        return self.__email

    @property
    def cart(self):
        return self.__cart   

    def get_user_data(self, *args):
        if not args:
            return {"first_name" : self.__first_name , "last_name": self.__last_name , "birth_date": self.__birth_date, "phone": self.__phone , "email": self.__email , "password": self.__password} 
        user_data = {}
        for arg in args:
            user_data[arg] = getattr(self,arg)
        return user_data

    def get_user_data_no_passwd(self):
        return {"first_name" : self.__first_name , "last_name": self.__last_name , "birth_date": self.__birth_date, "phone": self.__phone , "email": self.__email}

    def get_user_data_with_cart(self):
        return {"first_name" : self.__first_name , "last_name": self.__last_name , "birth_date": self.__birth_date, "phone": self.__phone , "email": self.__email , "cart":self.__cart} 

    @classmethod
    def convert_from_doc(cls,doc):
        return User(doc['first_name'],doc['last_name'],doc['birth_date'],doc['phone'],doc['email'] ,doc['password'])
        

