from itertools import count
from flask import Blueprint,request,jsonify
from src.config import MONGODB_URI
from pymongo import MongoClient
from src.modules.PyShuffle import PyShuffle
from src.modules.Pagination import Pagination
from datetime import datetime
from typing import List,Dict
from src.modules.Serializer import Serializer

crd = Blueprint('crd',__name__,url_prefix="/api/shuffle")
client = MongoClient(MONGODB_URI)
db = client.shuffle_mongo.db

@crd.post('/<text>')
def shuffle(text):
    ip_address = request.environ.get('HTTP_X_FORWARDED_FOR',request.remote_addr)
    shuffled = PyShuffle(text).shuffle()

    result:List = Serializer(['text']).dump(list(db.find({'ip_address':ip_address})))
    count = 0
    
    for element in result:
        if element['text'] == text:
            count += 1

    print(count)
    db_response = db.insert_one({
        'ip_address':ip_address,
        'text':text,
        'shuffled_result':shuffled,
        'shuffled_count':None,
        'shuffled_at':datetime.now()
    })

    if db_response.inserted_id:
        return jsonify({'error':False,'shuffled_result':shuffled}),200
    return jsonify({'error':True,'message':"something went wrong"}),500

@crd.get('/')
def get_all():
    ip_address = request.environ.get('HTTP_X_FORWARDED_FOR',request.remote_addr)

    try:
        page:int = int(request.args.get('page',1))
        limit:int = int(request.args.get('limit',10))
    except:
        return jsonify({'error':True,'message':"page and limit must be integers"}),400
    
    needed_attributes:List = ['_id','ip_address','text','shuffled_result','shuffled_at']
    result:List = Serializer(needed_attributes).dump(list(db.find({'ip_address': ip_address}).sort('_id')))
    pagination_result:Dict = Pagination(result,page,limit).meta_data()

    return jsonify({'error':False,'data':pagination_result}),200