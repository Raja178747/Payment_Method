from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash  
from database import init_db
# from flask_jwt_extended import JWTManager
import secrets
from models import create_user, get_user_by_username ,get_user_by_id, update_user_balance,add_transaction_update,add_transaction,get_transactions
from flask_cors import CORS
from datetime import timedelta

app = Flask(__name__)
CORS(app)
init_db(app)
jwt = JWTManager(app)


app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')
    
    user = get_user_by_username(username)
    if user:
        return jsonify({"message": "User already exists."}), 400

    user_id = create_user(username, email, phone, password)
    return jsonify({"user_id": user_id}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = get_user_by_username(username)
    if user and check_password_hash(user['password'], password):
        access_token = create_access_token(identity=str(user['_id']))
        return jsonify(access_token=access_token), 200
    return jsonify({"message": "Invalid credentials."}), 401



@app.route('/wallet/balance', methods=['GET'])
@jwt_required()
def get_wallet_balance():
    current_user = get_jwt_identity()
    print(f"Current user ID: {current_user}")
    user = get_user_by_id(current_user)

    return jsonify({"wallet_balance": user['wallet_balance']}), 200

@app.route('/wallet/add', methods=['POST'])
@jwt_required()
def add_money():
    current_user = get_jwt_identity()
    data = request.json
    amount = data.get('amount')

    update_user_balance(current_user, amount)
    add_transaction_update(current_user, {"type": "credit", "amount": amount})
    
    return jsonify({"message": "Money added successfully."}), 200

@app.route('/wallet/transfer', methods=['POST'])
@jwt_required()
def transfer_money():
    current_user = get_jwt_identity()  
    data = request.json
    recipient_username = data.get('recipient_username')
    amount = data.get('amount')

    sender = get_user_by_id(current_user)
    recipient = get_user_by_username(recipient_username)

    if not recipient:
        return jsonify({"message": "Recipient not found."}), 404

    if sender['wallet_balance'] < amount:
        return jsonify({"message": "Insufficient balance."}), 400

    update_user_balance(current_user, -amount)
    update_user_balance(recipient['_id'], amount)

    add_transaction(sender['_id'], recipient['_id'], amount, "successful")  
    add_transaction(recipient['_id'], sender['_id'], amount, "successful") 

    return jsonify({"message": "Transfer successful."}), 200


@app.route('/wallet/transactions', methods=['GET'])
@jwt_required()
def get_user_transactions():
    
    current_user_id = get_jwt_identity()  
    
    transactions = get_transactions(current_user_id)  
    print(transactions,"transactions")
    
    return jsonify([{
        "sender": str(transaction["sender"]),
        "recipient": str(transaction["recipient"]),
        "amount": transaction["amount"],
        "timestamp": transaction["timestamp"],
        "status": transaction["status"]
    } for transaction in transactions]), 200


if __name__ == '__main__':
    app.run(debug=True)
