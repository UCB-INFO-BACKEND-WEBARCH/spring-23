import os
from bson import ObjectId
from flask import Flask, jsonify, request, make_response
import pymongo
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from dotenv import load_dotenv

load_dotenv()
# Initialize the Flask app
app = Flask(__name__)

# Set a secret key for JWT token encryption
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Initialize the PyMongo extension
mongo = pymongo.MongoClient(os.getenv('MONGO_URI'))
db_name = os.getenv('MONGO_DBNAME')
db = mongo[db_name]  # Name of your database
col = db[db_name]

# Step 3: Registering and logging in users
# Create a route for registering new users
@app.route('/register', methods=['POST'])
def register():
    # Get user data from request body
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    quote = request.json['quote']

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Check if user already exists
    if col.find_one({'email': email}):
        return jsonify({'message': 'User already exists'}), 400

    # Insert new user into database
    user_id = col.insert_one({
        'name': name,
        'email': email,
        'password': hashed_password, # Not storing the original password
        'quote': quote
    })
    return jsonify({'message': 'User registered successfully'}), 201

# Create a route for logging in
@app.route('/login', methods=['POST'])
def login():
    # Get user data from request body
    email = request.json['email']
    password = request.json['password']

    # Check if user exists in database
    user = col.find_one({'email': email})
    # The HTTP WWW-Authenticate response header defines the HTTP authentication methods ("challenges") that might be used to gain access to a specific resource.
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    # Check if password is correct
    if check_password_hash(user['password'], password):
        # Create JWT token
        token = jwt.encode({
            'user_id': str(user['_id']),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24) # Setting expiry for token to 24 hours
        }, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token}), 200

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

# Step 4: Securing routes and services with JWT token authentication
# Create a decorator function for verifying the JWT token - This will be the auth middleware
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            token = str.replace(str(token), 'Bearer ', '')
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=["HS256"])
            print(data)
            current_user = col.find_one({'_id': ObjectId(data['user_id'])})
            print(current_user)
        except:
            return jsonify({'message': 'Unauthorized'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

# Create a secured route that requires JWT token authentication
@app.route('/protected')
@token_required
def protected(current_user):
    return jsonify({'message': 'This is a protected route', 'name': current_user['name'], 'quote': current_user['quote']})

# Step 5: Running the Flask app
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5050)
