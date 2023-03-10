# Import the Flask module
from flask import Flask, request

# Function to check if the input is numeric or not


def checkInput(num1: str, num2: str) -> float | str:
    try:
        return float(num1), float(num2), None
    except:
        return None, None, "Invalid Input"


# Create a Flask application object
app = Flask(__name__)

# Route for add - GET
@app.route("/add/<num1>/<num2>", methods=["GET"])
def add(num1, num2):
    num1, num2, errorVal = checkInput(num1, num2)
    if errorVal is not None:
        return "Invalid Input - Only numbers accepted", 400
    return {"answer": [str(num1 + num2)]}, 200

# Route for subtract - POST


@app.route("/sub", methods=["POST"])
def sub():
    num1 = request.form.get("num1")
    num2 = request.form.get("num2")
    num1, num2, errorVal = checkInput(num1, num2)
    if errorVal is not None:
        return "Invalid Input - Only numbers accepted", 400
    return {"answer": [str(num1 - num2)]}, 200

# Route for mul - POST


@app.route("/mul", methods=["POST"])
def mul():
    num1 = request.get_json().get("num1")
    num2 = request.get_json().get("num2")
    num1, num2, errorVal = checkInput(num1, num2)
    if errorVal is not None:
        return "Invalid Input - Only numbers accepted", 400
    return {"answer": [str(num1 * num2)]}, 200

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# python3 -m flask --app webserver run --host=0.0.0.0 --port=5050

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
