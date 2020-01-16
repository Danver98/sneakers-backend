import pymongo
from . import foots
from . import query
#import foots
#import query
from bson.objectid import ObjectId

dmitriy = pymongo.MongoClient('mongodb+srv://dmitriy:admin@cluster0-0jgxv.mongodb.net/test?retryWrites=true&w=majority')
#dmitriy = pymongo.MongoClient('mongodb://localhost:27017/')
fastfoot = dmitriy.Fastfoot
collection_foots = fastfoot.foots

def get_filters_result(param):
    query_param = query.Query()
    query_param.add_index(param)

    cursor = collection_foots.find(query_param.get_query(), {"_id": 1, "name": 1, "cost": 1, "text": 1, "img": 1})
    if len (query_param.get_sort()) > 0:
        cursor.sort(query_param.get_sort())

    foot_list = foots.FootList()

    for item in cursor:
        item["_id"] = str(item.get("_id"))
        foot_list.add_foot(item)

    return foot_list.get_all()

def get_one(obj_id):
    cursor = collection_foots.find_one({"_id": ObjectId(obj_id)})
    cursor["_id"] = str(cursor.get("_id"))

    return cursor

def update_param(obj_id, key, value):
    collection_foots.update({"_id": ObjectId(obj_id)}, {"$set": {key: value}})

def update_count(obj_id, step):
    update_param(obj_id, "count", get_one(obj_id).get("count") + step)

def get_search_result(param):
    query_words = param["query"].split('%')

    query_str = " ".join(query_words)

    cursor = collection_foots.find({"$text": {"$search": query_str}}, {"_id": 1, "name": 1, "cost": 1, "text": 1, "img": 1})

    foot_list = foots.FootList()

    for item in cursor:
        item["_id"] = str(item.get("_id"))
        foot_list.add_foot(item)

    return foot_list.get_all()