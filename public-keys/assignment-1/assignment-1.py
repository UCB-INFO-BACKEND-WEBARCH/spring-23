# Imports
from flask import Flask, jsonify, request
import json

# Initiating Flask App
app = Flask(__name__)

# Function that returns a JSON for command and messaage nested within the "data" key according to the prompt


def createReturnMessage(message, command=None):
    return jsonify({"data": {"command": command, "message": message}})


@app.route("/message", methods=["POST"])
def handleChatbotMessage():
    try:
        # Get message from the incoming JSON which is nested into the "data" key
        chatbotInput = request.get_json()['data']['message']
        # Removing unwanted spaces from the starting and ending of the "message" string
        chatbotInput = chatbotInput.strip(" ")
        # Returning an error if the string was empty
        if len(chatbotInput) == 0 or chatbotInput is None:
            return createReturnMessage("Error: Empty input"), 400
        # Returning the message back if the message didn't have the "/" at the start
        if chatbotInput[0] != "/":
            return createReturnMessage(chatbotInput), 200
        # Splitting /command and message from "/command message"
        messageParts = chatbotInput.split(" ", 1)
        # Getting command from "/command" and assigning message part to a new variable for easier reference
        command, message = messageParts[0][1:], messageParts[1]
        # Handling the case if command or message are emoty or invalid
        if len(command) == 0 or len(message) == 0 or command is None or message is None:
            return createReturnMessage("Error: Invalid input"), 400
        # Returning the final result
        return createReturnMessage(message, command), 200
    except:
        return createReturnMessage("Error: Something went wrong"), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
