# Authorizing our API endpoints in Flask

## Why do we need authorization for our API calls?

- When we create an API, we want to ensure that only authorized users can access certain parts of the API or perform certain actions. 
- Authorization helps us to restrict access to resources, prevent unauthorized changes to data, and protect sensitive information. 
- Without proper authorization, any user could access and modify data, which could lead to security breaches or unauthorized actions.

## How does authorization usually work? What are different ways that are commonly used to authorize API calls?

Authorization usually works by generating and verifying tokens that are associated with a user's account. When a user logs in, the server generates a unique token that is stored on the client-side. This token is then used to authenticate subsequent requests made by the user.

There are several ways that are commonly used to authorize API calls:

1. <b>Basic Authentication</b>: This method sends the user's credentials (i.e., username and password) in the header of each request, which the server verifies before granting access to the requested resource.

2. <b>Token-Based Authentication</b>: This method involves generating a unique token that is stored on the client-side and is used to authenticate subsequent requests made by the user. The token is usually sent in the header of each request and is verified by the server.

3. <b>OAuth Authentication</b>: This method involves a third-party service (i.e., OAuth provider) that generates an access token, which is then used to authenticate requests made by the user. This method is commonly used for social login and allows users to authenticate using their existing social media accounts.

*What do you think are drawbacks of each method?*

## Other benefits of authorization like identifying user using the token etc

In addition to restricting access to resources and preventing unauthorized actions, authorization also allows us to identify the user making the request. This is because the token that is generated during the authentication process is unique to each user and can be used to identify the user when making subsequent requests.

Furthermore, tokens can also be used to store additional information about the user, such as their role or permissions. This information can then be used to restrict access to certain parts of the API based on the user's role or permissions. This helps to ensure that only authorized users can perform certain actions and reduces the risk of security breaches or unauthorized actions.

## Hands-on Demo

### High-level idea
We want to create an API that can only be accessed by registered users! Hence, we will create a `protected route` to do this.

Our `protected route` will only give a response if we send an `auth token` as part of the API `headers`. Our Flask server should then check for the validity of that token and then either do the requested action or return a `403: Unauthorized`.

To make things more interesting, we are gonna uniquely identify the user from the auth token and then send them data in association with that user.

While registering the user, we will ask the user to input a username, password and their favorite quote. Our API then will actually return the favorite quote of the registered user trying to make that call.

### Understanding the flow

- We would use MongoDB to store user credentials
- We would have three APIs in total: `register`, `login`, `protected`.
- `register` is a POST endpoint that would allow the user to register for the service. Their credentials will be stored into the database.
    - We would use encryption to encrypt their data using hashing it and only store the encrypted password!
- `login` is another POST endpoint that would take in user's credentials and check if the user exists and if the password is right. If the user is actually valid, we would return a `Bearer Token` as part of the response.
- `protected` is a GET call which expects the bearer token as part of the API request `headers` and verifies the header. If the token is valid, it will return the name of the user and their quote!

### Code outline

demo/
│
├── app.py
└── .env

In this lab, we also introduce the introduction of `.env` environment files. These files are used to store important and private API keys and other passwords etc that you need to run your code.

We don't add these files to the list of Git tracked files (check `.gitignore` of this repo). Each contributor can set up their own environment file locally and use that. This prevents these keys being pushed into the public domains like GitHub.

### .env

You can use the `.env.example` file to start using this code. Rename it to `.env` and edit the content to your details and passwords.

```
SECRET_KEY=secret-key-here
MONGO_URI=mongodb+srv://<user>:<password>@<ip>
MONGO_DBNAME=dbname-here
```

### Getting all requirements ready

For this lab, we would need to install a few prerequisites. You can use the `requirements.txt` file to install them all at once using `pip install -r requirements.txt`.

### Importing all libraries and functions

```
import os
from dotenv import load_dotenv
from bson import ObjectId
from flask import Flask, jsonify, request, make_response
import pymongo
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
```

We already know what `flask`, `pymongo`, `os`, `datetime` do. There are a lot of new libraries that we are using here. So let's go over them one-by-one:

1. `bson`: Allows for BSON (Binary JSON) encoding and decoding in Python. We will use this to access ObjectId of Mongo objects.
2. `werkzeug`: It is a WSGI library and we will use some of its features to encrypt and decrypt a password.
3. `jwt`: Allows us to encode and decode a `JSON Web Token`. JSON Web Token is a proposed Internet standard for creating data with optional signature and/or optional encryption whose payload holds JSON that asserts some number of claims. The tokens are signed either using a private secret or a public/private key.
4. `wraps`: We use it to create a decorator for our auth middleware.
5. `dotenv`: Library that allows us to interact with out env file.

### Initializing everything

```
# Loading our .env file to access our keys
# os.getenv(key_name)
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
```

### Register - POST

```
@app.route('/register', methods=['POST'])
def register():
    # Get user data from request body
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    quote = request.json['quote']

    # Hash the password
    hashed_password = generate_password_hash(password) # We use the default function imported above

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
```

### Login - POST

```
@app.route('/login', methods=['POST'])
def login():
    # Get user data from request body
    email = request.json['email']
    password = request.json['password']

    # Check if user exists in database
    user = col.find_one({'email': email}) # Call to Mongo to find object
    if not user:
        # The HTTP WWW-Authenticate response header defines the HTTP authentication methods ("challenges") that might be used to gain access to a specific resource.
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'}) # Returning an error response

    # Check if password is correct
    if check_password_hash(user['password'], password):
        # Create JWT token
        token = jwt.encode({
            'user_id': str(user['_id']),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24) # Setting expiry for token to 24 hours
        }, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token}), 200

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
```

### Auth Middleware using decorator

```
def token_required(f):
    @wraps(f) # Creates a wrapper for decorated
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
```
`@wraps` is a decorator in Python that is used to wrap a function and preserve its original attributes such as __name__, __doc__, __module__, etc.

In the context of the Flask app we just implemented, we used the @wraps decorator to wrap the decorated function with the token_required decorator function. This is done to preserve the original attributes of the decorated function, such as its name and docstring. This is important because if we don't use @wraps, the decorated function will lose its original attributes and make debugging and testing more difficult.

Here's an example of how `@wraps` works:

```
from functools import wraps

def my_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        print('Calling decorated function')
        return f(*args, **kwds)
    return wrapper

@my_decorator
def example():
    """Docstring for example function"""
    print('Called example function')

print(example.__name__) # Output: example
print(example.__doc__) # Output: Docstring for example function
```

### Protected - GET

```
@app.route('/protected')
@token_required
def protected(current_user):
    return jsonify({'message': 'This is a protected route', 'name': current_user['name'], 'quote': current_user['quote']})
```