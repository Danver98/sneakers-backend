from pymongo import MongoClient
from flask import current_app , g
COLLECTION_NAME = "users_collection"
DATABASE = "common_database"
ATTEMPTS = 3

def get_db_connection():
    if 'con' not in g:
        g.con = MongoClient(current_app.config['DATABASE_URI'])
        g.db = MongoClient(current_app.config['DATABASE_URI'])[DATABASE]
    return g.db

def get_col():
    if 'db' not in g:
        g.db = MongoClient(current_app.config['DATABASE_URI'])[DATABASE]
    return g.db[COLLECTION_NAME]


def get_definite_col(con_URI = None ,db_name = None , col_name = None):
    if con_URI is None:
        con_URI = current_app.config['DATABASE_URI']
    if db_name is None:
        db_name = DATABASE
    if col_name is None:
        col_name = COLLECTION_NAME
    return MongoClient(con_URI)[db_name][col_name]
 
     




def close_db_connetion(e = None):
    g.pop('db',None)
    con = g.pop('con',None)
    if con is not None:
        con.close()

def init_db(app):
    app.teardown_appcontext(close_db_connetion)
    pass
    

