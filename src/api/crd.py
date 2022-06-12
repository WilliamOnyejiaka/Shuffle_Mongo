from flask import Blueprint,request,jsonify
from src.config import MONGODB_URI
from pymongo import MongoClient

crd = Blueprint('crd',__name__,url_prefix="/api/shuffle")
client = MongoClient(MONGODB_URI)
db = client.shuffle_mongo

@crd.post('/')
def shuffle():
    return jsonify({'error':False,'data':"Shuffled"})