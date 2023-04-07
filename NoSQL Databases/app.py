from flask import Flask, request
import pymongo

app = Flask(__name__)

def mongoConnection():
    try:
        # change your <username> and <password> below to connect to the database
        client = pymongo.MongoClient("mongodb+srv://<username>:<password>@<your clister ip>")
        db = client["test"] # Name of your database
        col = db["testCol"] # Name of your collection
        return col
    except:
        return Exception('Error connecting to DB')

@app.route('/', methods=['POST', 'GET'])
def index():
    try:
        col = mongoConnection()
    except:
        return {"error": "Error connecting to DB"}, 400
    if request.method == 'POST':
        try:
            
            params = request.get_json()
            # title = params['title']
            # status = params['status']
            # record = {
            #     "title": title,
            #     "status": status
            # }
            try:
                res = col.insert_one(params)
                return {}, 201
            except:
                raise Exception('Insertion Failed')
        except:
            return {"error": "Something went wrong"}, 400
    elif request.method == 'GET':
        tasks = col.find({})
        if tasks is None:
            return {"result": []}, 200
        output = list()
        for task in tasks:
            output.append({"id": str(task["_id"]),
            "title": task["title"],
            "status": task["status"]})
        return {"result": output}, 200

@app.route('/<title>', methods=['GET', 'PUT', 'DELETE'])
def getTaskByTitle(title):
    try:
        col = mongoConnection()
    except:
        return {"error": "Error connecting to DB"}, 400
    if request.method == 'GET':
        try:
            task = col.find_one({"title": title})
            if task is None:
                return {}, 404
            return {"id": str(task["_id"]),
            "title": task["title"],
            "status": task["status"]}, 200
        except:
            return {"error": "Something went wrong"}, 400
    elif request.method == 'PUT':
        try:
            filter = {"title": title}
            updatedRecord = {}
            newParams = request.get_json()
            if newParams['title'] is not None:
                updatedRecord['title'] = newParams['title']
            if newParams['status'] is not None:
                updatedRecord['status'] = newParams['status']
            newRecord = { "$set": updatedRecord }
            col.update_one(filter, newRecord)
            return {}, 200
        except:
            return {"error": "Something went wrong"}, 400
    elif request.method == 'DELETE':
        try:
            filter = {"title": title}
            col.delete_one(filter)
            return {}, 200
        except:
            return {"error": "Something went wrong"}, 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)