from pymongo import MongoClient
from flask import current_app , g
COLLECTION_NAME = "users_collection"
DATABASE = "common_database"

def get_db_connection():
    if 'con' not in g:
        g.con = MongoClient(current_app.config['DATABASE_URI'])
        g.db = MongoClient(current_app.config['DATABASE_URI'])[DATABASE]
    return g.db

def get_col():
    if 'db' not in g:
        g.db = MongoClient(current_app.config['DATABASE_URI'])[DATABASE][COLLECTION_NAME]
    return g.db[COLLECTION_NAME]

"""
@app.teardown_appcontext
def close_db():
    db = g.pop('db',None)
    if db is not None:
        db.close()
"""
def close_db_connetion(e = None):
    g.pop('db',None)
    con = g.pop('con',None)
    if con is not None:
        con.close()

def init_db(app):
    app.teardown_appcontext(close_db_connetion)
    pass
    