# Imports
from flask import Flask, jsonify, request
import json

# Initiating Flask App
app = Flask(__name__)

# Function that creates an appropriate response JSON based on message and command
def createReturnMessage(message, command=None):
    return jsonify({"data": {"command": command, "message": message}})

# Execute Endpoint Handler
@app.route("/execute", methods=["POST"])
def handleShrugCommand():
    try:
        # Gets message and command from the JSON body nested wihtin "data"
        command, message = request.get_json()['data']['command'], request.get_json()['data'][
            'message']
        # Additional check to see if the command is infact "shrug"
        # This check is important as your Endpoint is still directly callable from outside the chatbot
        if command != "shrug":
            return createReturnMessage("Error: Not a Shrug Command"), 400
        # Adding the shrug emoji to the end of the message
        return createReturnMessage(message + '¯\_(ツ)_/¯', command), 200
    except:
        # Error handler in case the try block fails
        return createReturnMessage("Error: Something went wrong"), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5051, debug=True) # Running the shrug server on 5051
