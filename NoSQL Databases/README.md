# NoSQL Databases

## What are NoSQL databases? 
NoSQL databases, also known as "non-relational" databases, are databases that store and retrieve data without using a traditional structured query language (SQL) for defining and manipulating data. Instead, they use other methods to store and access data, such as key-value pairs, document-oriented storage, column-family, and graph databases. NoSQL databases are designed to handle large-scale, unstructured, and semi-structured data, making them particularly useful for big data applications and real-time web applications.

## SQL vs NoSQL databases
The main difference between NoSQL and SQL databases is their data model. While SQL databases use a structured data model that requires tables and columns to be predefined with a strict schema, NoSQL databases can store data in a variety of formats, including key-value pairs, document-oriented, column-family, and graph databases. NoSQL databases can handle large amounts of data, and their schema-less design allows for flexibility in data storage and retrieval.

## When to use NoSQL databases?
There are several scenarios where a NoSQL database might be a better choice than a traditional SQL database:

- Handling big data: NoSQL databases are designed to handle large-scale data, making them ideal for big data applications where scalability and performance are critical.
- Real-time web applications: NoSQL databases are often used in real-time web applications, where data needs to be accessed and processed quickly and efficiently.
- Unstructured data: If your data is unstructured or semi-structured, NoSQL databases can provide a more flexible approach to data storage and retrieval.
- Highly distributed environments: NoSQL databases are well-suited for highly distributed environments, where data needs to be stored and accessed across multiple servers or data centers.

## Some examples of NoSQL databases
Here are some examples of popular NoSQL databases:

- MongoDB: A document-oriented NoSQL database that is designed for flexibility and scalability.
- Cassandra: A column-family NoSQL database that is designed for handling large amounts of data across multiple data centers.
- Redis: A key-value store NoSQL database that is designed for fast data retrieval and processing.
- Neo4j: A graph-based NoSQL database that is designed for storing and querying connected data.

For people who are interested in diving deeper into NoSQL databases, this [link](https://www.mongodb.com/nosql-explained/nosql-vs-sql) might be helpful. And this is a quick [intro](https://www.guru99.com/nosql-tutorial.html#:~:text=NoSQL%20Database%20is%20a%20non,and%20real%2Dtime%20web%20apps.) to NoSQL databases.

## Hands-on Demo
In today's lab we covered the basics of NoSQL databases, how they are different to RDBMS/SQL databases like MySQL we have used in the past.
We then proceeded to create a NoSQL database on cloud using [MongoDB Atlas](cloud.mongodb.com) which allows setting up free shared clusters online.
You can create an account, and create a new cluster with a username and password.
We will then use this cluster alongside its authentication mechanisms for connecting our application to the database.

Our database and the collection will be hosted within this cluster.

## Connecting to our MongoDB Cluster
Before we begin, please install `pymongo` and `pymongo[srv]` using `pip3 install pymongo` and `pip3 install "pymongo[srv]"`.

```
# Like we did in our MySQL webserver files, we create a function that connects to MongoDB
def mongoConnection():
    try:
        # change your <username> and <password> below to connect to the database
        client = pymongo.MongoClient("mongodb+srv://<username>:<password>@cluster0.0yqkv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client["test"] # Name of your database
        col = db["testCol"] # Name of your collection
        return col
    except:
        return Exception('Error connecting to DB')
```
We set up a client using pymongo's MongoClient. The URL in this line can be obtained using your MongoDB atlas dashboard. There should be a `connect` button right next to your cluster which should give you this URL and relevant commands for Python.

<strong>Please change your username and password in this line to reflect your credentials.

We then connect to our database using `client['test']` where `test` is the name of the database and to our collection within that database using `db['testCol']` where `testCol` is the name of our collection.

## Using NoSQL/MongoDB instead of MySQL
The setup of the Flask webapp will exactly be the same as we have done throughout this course at various instances. However, the way we interact with MongoDB for CRUD operations is a bit different

### Insertion into MongoDB
Since MongoDB (NoSQL databases in general) uses an object model, we create a JSON object for our resource and then use that for insertion. We don't insert anything into a table based on a fixed schema.

```
params = request.get_json()
title = params['title']
status = params['status']
record = {
    "title": title,
    "status": status
    }
res = col.insert_one(record)
return {}, 201    
```
We first create `record` object using our parameters we got from our JSON body and then we use `insert_one` command to insert our record into the collection.

### Querying from MongoDB
<ol>
<li> Query all records</li>
To query all records, we use `col.find({})` where `col` is our collection

```
tasks = col.find({})
```

We then use an iterator to convert this reponse into a list of object that is suitable and readable for return.

```
output = list()
for task in tasks:
    output.append({"id": str(task["_id"]),
    "title": task["title"],
    "status": task["status"]})
return {"result": output}, 200
```
<li> Query filtered records</li>
To query a record based on a certain parameter or condition, we can directly embed our condition into the `find()`.

```
task = col.find_one({"title": title})
```

Here, we are filtering our results based on the `title`. Please note that the filters you provide are keys within your objects in the collection.
Now we can process this task to make it readable and return it.

```
return {"id": str(task["_id"]),
    "title": task["title"],
    "status": task["status"]}, 200
```

## Updating in MongoDB
Like the READ method, UPDATE is also fairly simple in MongoDB as compared to MySQL and relies on the properties (keys) of an object.
We use a `filter` which tells the database which records to look into. This is basically the equivalent to our `WHERE` keyword in MySQL.

```
filter = {"title": title}
updatedRecord = {}
newParams = request.get_json()
if newParams['title'] is not None:
    updatedRecord['title'] = newParams['title']
if newParams['status'] is not None:
    updatedRecord['statis'] = newParams['status']
```
We are filtering our tasks here using the `title` tag. We query all the tasks with the title that we input as part of our API call.
We also expect the new title or status from the API body. We then combine the `filter` and the new information (`updatedRecord`).

```
newRecord = { "$set": updatedRecord }
col.update_one(filter, newRecord)
return {}, 200
```
We then use `update_one` which takes in the filter and the `newRecord` which is nothing but our `updatedRecord` tied in with the `"$set"` keyword which tells the database to replace or `set` the updatedRecord in place of the filtered record.
<i>This updates the first record that matches our filter specs.</i>

## Deleting in MongoDB
We can delete a record using the `filter` that we have used for GetByID and UPDATE methods above.

```
filter = {"title": title}
col.delete_one(filter)
return {}, 200
```
We use `delete_one` to delete the <i>first instance</i> of the filtered records.