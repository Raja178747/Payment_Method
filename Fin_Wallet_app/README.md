# Flask Wallet Application

This is a Flask-based wallet application that supports user registration, login, wallet management (add money, check balance, transfer money), and transaction history.

## Features
- User Registration
- User Login with JWT authentication
- Wallet Management
  - Check wallet balance
  - Add money to the wallet
  - Transfer money between users
- Transaction History

# Install the requirements:
pip install -r requirements.txt

# Set up your environment variables in a .env
MONGO_URI=your_mongo_uri

# Run the application:
python run.py