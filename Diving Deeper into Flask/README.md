# Lab 3 - Diving Deeper into Flask (Feb 10, 2023)

## Quick Recap

```
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

# Run the application
if __name__ == "__main__":
    app.run(debug=True)
```

- `app = Flask(__name__)` creates an instance of the Flask class and assigns it to the app variable.
- The `@` symbol is used to define a `decorator` for a Flask route. In the case of Flask, the decorator is used to associate a function (also known as a view function or handler) with a specific URL route.
- `@app.route("/")` is the decorator that tells Flask that the index() function should handle HTTP requests to the root URL ("/")
- The HTTP methods that the route can allow are passed as an array as part of the param to the decorator. `@app.route("/create", methods=["POST"])` creates a `/create` route that allows a POST call.
- The three most common methods to get data as part of an API are `URL Params`, `Query Params` and `Request Body`.
- `/add/<num1>/<num2/` allows the client to send two URL Parameters as part of the `/add` route. You can directly access these values by recieving them as parameters to your handler: `def update(id)` for `/delete/<id>`. You can also assign them default values - `def update(id=5)`

## Working with other types of data

### Query Parameters

API Query parameters can be defined as the optional key-value pairs that appear after the question mark in the URL. Basically, they are extensions of the URL that are utilized to help determine specific content or action based on the data being delivered.

They are appended to the end of a route using the `?` keyword. For example: `/delete?id=10` could be another way to access the id for the delete endpoint in the above code.

If you want to add multiple parameters, we use the `&` keyword. `/add?num1=10&num2=5`. The

Query Parameters can be accessed in your Flask code by using the `request` function and the `args` method from it.

When we use request to fetch data from the API request, we always get an `Immutable MultiDict`. We can then use key indexing to get the value for the desired parameter.

```
@app.route("/delete", methods=["DELETE"])
def delete():
    recordID = request.args.get("id")
    return f"{recordID} deleted from DB"
```

### Request Body

Request bodies are used to send a buffer of data in different formats to the server. We need bodies because the size of the header of an API is limited. But what does that mean? The number of Query Parameters, Headers and URL Parameters that you can send as part of an API call are limited by size.

Also, The other parameters are public and are visible as part of the URL itself. So body presents a safer way to send that data out (preferably in an encrypted form).

Similar to `Query Parameters`, Request Bodies can be accessed in flask using the `request` function. If your Request Body is just data buffer, you can use `request.get_data()` method to access your data. If it is a json, you can specifically use `request.get_json()`.

The `get_data` method gives us `bytes` of data while the `get_json` method gives us a `dict`.

```
@app.route("/post", methods=["POST"])
def delete():
    name = request.get_json().get("name")
    return f"Hi, {name}!"
```

### Files and Forms

You can also send data as part of your API call through a form or a file. We again use the `request` method for accessing the information for the two.

```
# Accessing Files

@app.route("/file", methods=["POST"])
def file():
    uploadedFile = request.files.get('name')
    return f"{uploadedFile.filename} uploaded!"
```

For files, we use the `request.files` method. We can then access its content like a regular file.

```
# Accessing Forms

@app.route("/file", methods=["POST"])
def form():
    name = request.form.get('name')
    return f"Hi, {name}!"
```

For forms, we use the `request.form` method. Similar to `request.args`, this again gives us an `ImmutableMultiDict` and we can use key indexing to accesssing the data we need.

## What method to use and when?

The best practice is to choose the appropriate method depending on the use case and the type of data that you want to pass to the server.

- When accessing a specific resource on the server, use URL parameters.
- When filtering or sorting data on the server, use query parameters.
- When passing large amounts of data to the server, use the request body.

## HTTP Response Codes

Response codes are used in HTTP to communicate the outcome of a request made by a client to a server. They provide a standardized way for the server to indicate the result of the request, and provide useful information for the client to handle the response appropriately.

Why use them?

1. Communication of Request Result: Response codes allow the server to clearly communicate whether a request was successful or not, and if not, why. This helps the client to understand the result of the request and take appropriate action.

2. Error handling: Different response codes indicate different types of errors. For example, a 404 Not Found response code indicates that the requested resource could not be found, while a 400 Bad Request response code indicates that the request was invalid. This allows the client to handle errors more effectively.

3. Caching: Response codes such as 304 Not Modified can be used to indicate that the resource has not been modified since the last request, allowing the client to use a cached version of the resource rather than requesting it again.

4. Restful API Design: Response codes play an important role in RESTful API design, as they are used to communicate the outcome of resource operations such as creation, retrieval, updating, and deletion.

Following is a list of appropriate and most-used response codes for each HTTP CRUD method:

1. GET

   1. 200 OK: The request was successful, and the resource was retrieved.
   2. 204 No Content: The request was successful, but there is no representation to return (i.e. the response is empty).
   3. 304 Not Modified: The resource has not been modified since the last request.

2. POST

   1. 201 Created: The request was successful, and a resource was created.
   2. 400 Bad Request: The request was invalid or cannot be served.
   3. 409 Conflict: The request could not be completed due to a conflict with the current state of the resource.

3. PUT

   1. 200 OK: The request was successful, and the resource was updated.
   2. 201 Created: The request was successful, and a new resource was created.
   3. 204 No Content: The request was successful, but there is no representation to return (i.e. the response is empty).

4. DELETE
   1. 200 OK: The request was successful, and the resource was deleted.
   2. 204 No Content: The request was successful, but there is no representation to return (i.e. the response is empty).
   3. 404 Not Found: The resource could not be found.

## API Responses in Flask

Return type in Flask is restricted to the following: string, tuple, Response instance, or WSGI callable.

The default return type in Flask is a `Response` object. Most of the times, we don't have to create one manually as Flask does that for us. For example, when string type response object is returned, Flask automatically converts that into the required format.

The `Response` object allows us to set data, headers and status code inside it. The order is `data, status_code, headers`.

```
from flask import jsonify

@app.route("/api/endpoint", methods=["GET"])
def endpoint():
    data = {"message": "Hello, World!"}
    headers = {"Content-Type": "application/json"}
    return data, 200, headers
```

In this example, the `jsonify` function is used to create a JSON response object from the `data` dictionary. The 200 status code indicates a successful response. The response object and the status code are then returned from the endpoint function using the return statement. We are also setting additional `headers` as part of the response.
