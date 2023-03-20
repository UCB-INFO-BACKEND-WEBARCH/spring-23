# Imports
from flask import Flask, jsonify, request
import json
import requests

# Initiating Flask App
app = Flask(__name__)

# Function to read data from file
def getDataFromFile():
    file = open('serverMapping.json')
    data = json.load(file)
    file.close()
    return data

# Write new JSON to file
def writeToFile(quotesData):
    with open("serverMapping.json", "w") as f:
        json.dump(quotesData, f)
        f.close()

# Function that checks if a dedicated server for a command exists
# If it does, handles the nested post call to /execute endpoint
# Else, returns normal message from Assignment 1
def handleByCommand(message, command):
    serverList = getDataFromFile()
    if command not in serverList:
        return createReturnMessage(message, command)
    if serverList[command][-1] != "/":
        urlPath = serverList[command] + "/execute"
    else:
        urlPath = serverList[command] + "execute"
    jsonBody = {"data": {"command": command, "message": message}}
    return requests.post(urlPath, json=jsonBody).json()
    # Function that returns a JSON for command and messaage nested within the "data" key according to the prompt

# Function that handles the creation of the output JSON in the desired format
def createReturnMessage(message, command=None):
    return jsonify({"data": {"command": command, "message": message}})

# Handler for /message endpoint
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
        return handleByCommand(message, command)
    except:
        return createReturnMessage("Error: Invalid input"), 400

# Handler for /register endpoint
@app.route("/register", methods=["POST"])
def handleRegisterCall():
    try:
        # Getting the command and the server url from JSON body
        serverCommand, serverURL = request.get_json()['data']['command'], request.get_json()['data'][
            'server_url']
        # Removing any redundant whitespace
        serverURL = serverURL.strip(" ")
        # Checking if command or url are invalid or not
        if serverCommand is None or serverCommand == "" or serverURL is None or serverURL == "":
            return createReturnMessage("Error: Invalid Input"), 400
        # Getting current list of server and url mapping from file
        currentServers = getDataFromFile()
        # Adding/Updating URL for the command
        currentServers[serverCommand] = serverURL
        # Writing to file
        writeToFile(currentServers)
        # Returning the expected "saved" message
        return createReturnMessage("saved", serverCommand)
    except:
        return createReturnMessage("Error: Something went wrong"), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
