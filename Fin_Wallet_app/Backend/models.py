from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database import mongo
from bson import ObjectId
from datetime import datetime

def create_user(username, email, phone, password):
    hashed_password = generate_password_hash(password)
    user_id = mongo.db.users.insert_one({
        "username": username,
        "email": email,
        "phone": phone,
        "password": hashed_password,
        "wallet_balance": 0
    }).inserted_id
    return str(user_id)


def get_user_by_username(username):
    return mongo.db.users.find_one({"username": username})


def get_user_by_id(user_id):
    user_id = ObjectId(user_id)
    return mongo.db.users.find_one({"_id": user_id})


def update_user_balance(user_id, amount):
    user_id = ObjectId(user_id)
    mongo.db.users.update_one({"_id": user_id}, {"$inc": {"wallet_balance": amount}})

def add_transaction_update(user_id, transaction):
    user_id = ObjectId(user_id)
    mongo.db.users.update_one({"_id": user_id}, {"$push": {"transactions": transaction}})

def add_transaction(sender_id, recipient_id, amount, status):
    transaction = {
        "sender": sender_id,
        "recipient": recipient_id,
        "amount": amount,
        "timestamp": datetime.utcnow(),
        "status": status
    }
    mongo.db.transactions.insert_one(transaction)

def get_transactions(user_id):
    user_id = ObjectId(user_id)
    print(user_id)  
    transactions = list(mongo.db.transactions.find({
        "$or": [
            {"sender": user_id},
            {"recipient": user_id}
        ]
    }))
    
    print("Transactions found:", transactions)
    
    return transactions