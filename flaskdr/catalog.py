import queries
from flask import Flask, jsonify, request, Blueprint

#app_catalog = Flask(__name__)
app_catalog = Blueprint('catalog',__name__,url_prefix ='/main')

@app_catalog.route('/catalog/', methods = ['POST', 'GET'])
def get_catalog():
    return jsonify(queries.get_filters_result(request.args))

@app_catalog.route('/catalog/<str_id>/', methods = ['POST', 'GET'])
def get_choose(str_id):
    return jsonify(queries.get_one(str_id))

@app_catalog.route('/catalog/search/', methods = ['POST', 'GET'])
def get_search():
    return jsonify(queries.get_search_result(request.args))

#app_catalog.run(debug = True)