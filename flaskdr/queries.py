import pymongo
from . import foots
from . import query
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

def get_search_result(param):
    query_list = param["query"].split('%')

    cursor = collection_foots.find({}, {"_id": 1, "name": 1, "cost": 1, "text": 1, "img": 1})

    foot_list = foots.FootList()

    for item in cursor:
        item["_id"] = str(item.get("_id"))
        foot_list.add_foot(item)

    return foot_list.get_all()