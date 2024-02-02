from pymongo import MongoClient
from bson.objectid import ObjectId
import urllib.parse

def get_mongo_client():
    username = "rohitchavan6361"
    password = "Rohit@4521"
   
    username = urllib.parse.quote_plus(username)
    password = urllib.parse.quote_plus(password)
    client = MongoClient(f"mongodb+srv://{username}:{password}@cluster0.1bnlbko.mongodb.net/")
    return client

def get_products_collection():
    client = get_mongo_client()
    return client["ecommerce"]["products"]

def get_orders_collection():
    client = get_mongo_client()
    return client["ecommerce"]["orders"]

def insert_order(order_data):
    orders_collection = get_orders_collection()
    order_id = orders_collection.insert_one(order_data).inserted_id
    return str(order_id)

def insert_dummy_products(products_collection):
    dummy_products = [
        {"name": "TV", "price": 499.99, "quantity": 50},
        {"name": "Laptop", "price": 899.99, "quantity": 30},
        {"name": "Smartphone", "price": 299.99, "quantity": 100},
        
    ]

 
    products_collection.insert_many(dummy_products)

def query_products(products_collection, filters=None, limit=10, offset=0):
    query = filters or {}

   
    records = products_collection.find(query).limit(limit).skip(offset)


    total = products_collection.count_documents(query)

    return {
        "records": list(records),
        "total": total
    }

