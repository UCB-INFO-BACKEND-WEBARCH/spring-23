from flask import Flask, request, Response, jsonify
import json

app = Flask(__name__)

# Helper function that gets the map from the file


def getDataFromFile():
    file = open('locations.json')
    data = json.load(file)
    locationMap = data['userLocation']
    file.close()
    return locationMap

# Helper function that checks if the name (key) exists in the file


def getResult(name, userLocations=None):
    if userLocations is None:
        userLocations = getDataFromFile()
    if name is not None:
        result = {key: value for key, value in userLocations.items()
                  if key == name}
    else:
        return jsonify({
            "error": "Invalid Request - No Name Parameter"
        }), 400
    if result == {}:
        return {}, 204
    return jsonify(result), 200

# API endpoint that allows multiple routes in one and uses different input types
@app.route("/arg")
@app.route("/arg/<name>", methods=['GET'])
def arg(name=None):  # name takes the value from URL param
    if request.args:  # request.arg stores the Request Params
        name = request.args.get('name')
    elif request.data:  # request.data stores the Body
        name = request.get_json()['name']
    return getResult(name)

# API endpoint to handle put and delete methods
@app.route("/update/<name>", methods=["PUT", "DELETE"])
def update(name):
    statusCode = 400
    if request.method == "PUT":
        userLocationData = getDataFromFile()
        if name in userLocationData.keys():
            statusCode = 200
        else:
            statusCode = 201
        userLocation = request.get_json().get("location")
        data = {}
        userLocationData[name] = userLocation
        data['userLocation'] = userLocationData
        with open("locations.json", "w") as f:
            json.dump(data, f)
        return jsonify({
            "name": name,
            "location": userLocation
        }), statusCode
    if request.method == "DELETE":
        pass # Should be very similar to PUT case

# API endpoint that gets name key as part of form-data
@app.route("/arg/form", methods=['GET'])
def getWithForm():
    name = request.form.get('name')
    return getResult(name)

# API endpoint that allows a new file upload and then uses that for finding a name
@app.route("/arg/file", methods=['GET'])
def getWithFile():
    locationsFile = request.files.get('locationFile')
    fileExtension = locationsFile.filename.split('.')[1]
    if fileExtension != "json":
        return {
            "error": "Invalid File Type"
        }, 400
    if locationsFile is None:
        return {
            "error": "No locations file provided"
        }, 400
    data = json.load(locationsFile)
    userLocations = data['userLocation']
    name = request.form.get('name')
    return getResult(name, userLocations)


# Run the server using one of the following ways:

# python3 -m flask --app week-3 run --host=0.0.0.0 --port=5050

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=8000)
