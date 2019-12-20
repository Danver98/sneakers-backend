from . import queries
from flask import Flask, jsonify, request, Blueprint

#app_catalog = Flask(__name__)
app_catalog = Blueprint('catalog',__name__,url_prefix ='/main')

@app_catalog.route('/catalog/')
def get_catalog():
    return jsonify(queries.get_result(request.args))

@app_catalog.route('/catalog/<str_id>/')
def get_choose(str_id):
    return jsonify(queries.get_one(str_id))

#app_catalog.run(debug = True)