from flask import Flask, jsonify, request
import json

app = Flask(__name__)


def getDataFromFile():
    file = open('quotes.json')
    data = json.load(file)
    file.close()
    return data


def writeToFile(quotesData):
    with open("quotes.json", "w") as f:
        json.dump(quotesData, f)
        f.close()


def returnError():
    raise ValueError("Invalid Input")


def isValidCall(day=None, method="GET"):
    print("Day 2", day)
    acceptableDays = ['sunday', 'monday',
                      'tuesday', 'thursday', 'friday', 'saturday']

    if day is None:
        if method == "PUT" or method == "DELETE":
            returnError()
    else:
        if day.lower() not in acceptableDays:
            returnError()
    return True


def handleGetAll():
    quotesData = getDataFromFile()
    if quotesData is None or quotesData == {}:
        return {}, 204
    return jsonify(quotesData), 200


def handleGetByID(day):
    quotesData = getDataFromFile()
    if day not in quotesData.keys():
        return {}, 204
    return {day: quotesData[day]}, 200


def handleDeleteQuote(day):
    quotesData = getDataFromFile()
    if day not in quotesData.keys():
        return {}, 404
    quotesData.pop(day)
    writeToFile(quotesData)
    return {}, 200


def handleUpdateOrCreateQuote(day, quote):
    if type(quote) is not str:
        returnError()
    quotesData = getDataFromFile()
    status = 201
    if day in quotesData.keys():
        status = 200
    quotesData[day] = quote
    writeToFile(quotesData)
    return {day: quote}, status


@app.route("/", methods=["GET", "POST"])
@app.route("/<day>", methods=["GET", "PUT", "DELETE"])
def quotesAPI(day=None):

    try:
        if day is None:
            if request.method == "POST":
                day = request.get_json().get("day")
        isValidCall(day, request.method)
        if request.method == "GET":
            if day is None:
                return handleGetAll()
            else:
                return handleGetByID(day)
        elif request.method == "POST":
            quote = request.get_json().get("quote")
            day = request.get_json().get("day")
            if day is not None and quote is not None:
                return handleUpdateOrCreateQuote(day, quote)
            else:
                returnError()
        elif request.method == "PUT":
            quote = request.get_json().get("quote")
            if quote is not None:
                return handleUpdateOrCreateQuote(day, quote)
            else:
                returnError()
        else:
            return handleDeleteQuote(day)
    except:
        return {"error": "Something went wrong!"}, 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
