# Import the Flask module
from flask import Flask

# Create a Flask application object
app = Flask(__name__)

# Define a route for the root URL
@app.route("/")
def index():
    return "Welcome to the Flask CRUD server!"

# Define a route for the "create" endpoint
@app.route("/create", methods=["POST"])
def create():
    # Code to create a new resource
    return "Resource created!"

# Define a route for the "read" endpoint
@app.route("/read/<id>", methods=["GET"])
def read(id):
    # Code to retrieve a resource
    return f"Resource with id {id} retrieved!"

# Define a route for the "update" endpoint
@app.route("/update/<id>", methods=["PUT"])
def update(id):
    # Code to update a resource
    return f"Resource with id {id} updated!"

# Define a route for the "delete" endpoint
@app.route("/delete/<id>", methods=["DELETE"])
def delete(id):
    # Code to delete a resource
    return f"Resource with id {id} deleted!"

# python3 -m flask --app webserver run --host=0.0.0.0 --port=5050

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=8000)
