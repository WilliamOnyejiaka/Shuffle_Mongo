from flask import Blueprint, request, jsonify
from src.config import MONGODB_URI
from pymongo import MongoClient
# from src.modules.PyShuffle import PyShuffle
from src.modules.shuffle import Shuffle
from src.modules.Pagination import Pagination
from datetime import datetime
from typing import List, Dict
from src.modules.Serializer import Serializer

crd = Blueprint('crd', __name__, url_prefix="/api/shuffle")
client = MongoClient(MONGODB_URI)
db = client.shuffle_mongo.db


@crd.post('/<text>')
def shuffle(text):
    ip_address = request.environ.get(
        'HTTP_X_FORWARDED_FOR', request.remote_addr)
    shuffled = Shuffle(text).shuffle()

    query = db.find_one({'ip_address': ip_address, 'text': text})
    
    if query:
        shuffle_details = Serializer(['text', 'shuffled_count', 'previous_shuffles']).serialize(query)

        shuffle_details['previous_shuffles'].append(shuffled)
        update_query = db.update_one({
            'ip_address': ip_address,
            'text':text
        }, {
                '$set': {
                    'shuffled_count': int(shuffle_details['shuffled_count'])+1,
                    'previous_shuffles': shuffle_details['previous_shuffles'],
                    'updated_at': datetime.now()
                }})
        if update_query.modified_count:
            return jsonify({'error': False, 'shuffled_result': shuffled,'message':"rust"}), 200
        return jsonify({'error': True, 'message': "something went wrong"}), 500

    db_response = db.insert_one({
        'ip_address': ip_address,
        'text': text,
        'latest_result': shuffled,
        'shuffled_count': 1,
        'previous_shuffles': [shuffled],
        'created_at': datetime.now(),
        'updated_at': None
    })

    if db_response.inserted_id:
        return jsonify({'error': False, 'shuffled_result': shuffled}), 200
    return jsonify({'error': True, 'message': "something went wrong"}), 500


@crd.get('/')
def get_all():
    ip_address = request.environ.get(
        'HTTP_X_FORWARDED_FOR', request.remote_addr)

    try:
        page: int = int(request.args.get('page', 1))
        limit: int = int(request.args.get('limit', 10))
    except:
        return jsonify({'error': True, 'message': "page and limit must be integers"}), 400

    needed_attributes: List = ['_id', 'ip_address', 'text','latest_result', 'shuffled_count', 'previous_shuffles','created_at','updated_at']
    result: List = Serializer(needed_attributes).dump(
        list(db.find({'ip_address': ip_address}).sort('_id')))
    pagination_result: Dict = Pagination(result, page, limit).meta_data()

    return jsonify({'error': False, 'data': pagination_result}), 200

@crd.delete('/')
def delete():
    ip_address = request.environ.get('HTTP_X_FORWARDED_FOR',request.remote_addr)
    query = db.delete_many({'ip_address':ip_address})

    if query:
        return jsonify({'error':False,'message':"deleted successfully"}),200
    return jsonify({'error':True,'message':"something went wrong"}),500
