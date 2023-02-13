"""
It's time to get your hands dirty and create your first Flask web server. To keep it simple, we will be creating a webserver that supports simple arithmetic operations - add/multiply/divide/subtract.

1. "add/<num1>/<num2>" - GET type - returns num1 + num2
2. "sub/<num1>/<num2>" - GET type - returns num1 - num2
3. "mul/<num1>/<num2>" - POST type - returns num1 * num2
4. "div/<num1>/<num2>" - POST type - returns num1/num2

Validations:
Input type - int/float/string (can be any value) - Needs checking and exception handling
Output type - string/float/number

Special cases:
Div - Denominator cannot be 0 (NaN)
"""


# Import the Flask module
from flask import Flask

# Function to check if the input is numeric or not


def checkInput(num1: str, num2: str) -> float | str:
    try:
        return float(num1), float(num2), None
    except:
        return None, None, "Invalid Input"


# Create a Flask application object
app = Flask(__name__)

# Route for the root URL


@app.route("/")
def index():
    return """
    <h2>Welcome to Lab 3 for INFO 153B/253B.</h2> 
    <p>You can use the following endpoints
    <ul>
    <li>add/< num1 >/< num2 > - <b>GET</b></li>
    <li>sub/< num1 >/< num2 > - <b>GET</b></li>
    <li>mul/< num1 >/< num2 > - <b>POST</b></li>
    <li>div/< num1 >/< num2 > - <b>POST</b></li>
    </ul>
    </p>
    """


# Route for add - GET
@app.route("/add/<num1>/<num2>", methods=["GET"])
def add(num1, num2):
    num1, num2, errorVal = checkInput(num1, num2)
    if errorVal is not None:
        return "Invalid Input - Only numbers accepted", 400
    return str(num1 + num2), 200

# Route for subtract - GET


@app.route("/sub/<num1>/<num2>", methods=["GET"])
def sub(num1, num2):
    num1, num2, errorVal = checkInput(num1, num2)
    if errorVal is not None:
        return "Invalid Input - Only numbers accepted", 400
    return str(num1 - num2), 200

# Route for mul - POST


@app.route("/mul/<num1>/<num2>", methods=["POST"])
def mul(num1, num2):
    num1, num2, errorVal = checkInput(num1, num2)
    if errorVal is not None:
        return "Invalid Input - Only numbers accepted", 400
    return str(num1 * num2), 200

# Route for dic - POST


@app.route("/div/<num1>/<num2>", methods=["POST"])
def div(num1, num2):
    if float(num2) == 0:  # Checking for denominator to be 0
        return "Invalid Input - Only numbers accepted", 400
    num1, num2, errorVal = checkInput(num1, num2)
    if errorVal is not None:
        return "Invalid Input - Only numbers accepted", 400
    return str(num1 / num2), 200

# python3 -m flask --app webserver run --host=0.0.0.0 --port=5050

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=8000)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
