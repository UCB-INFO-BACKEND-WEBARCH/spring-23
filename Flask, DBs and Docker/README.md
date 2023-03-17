# Docker + Postgres + Flask

In most real-world scenarios, you are required to store data in a database. There are many different options when it comes to choosing what database you want - `Cassandra`, `DynamoDB`, `MongoDB`, `MySQL`, `Postgres` are some of the many names that are widely used each day.

Today, we are going to have a fast-paced, hands-on session that combines together all the knowledge that we have of Flask, Docker and Docker Compose and tie it in with using a database (`Postgres`) with our application pretty quickly. This demo will also allow us to see the real-world use of Dockers and where they shine.

** Drumroll **

## Objective

We are going to create a simple application that allows CRUD operations on information around Cats. To keep out application simple, let's assume that our application only deals with 3 fields:

- `Name` of the cat
- `Color` of the cat
- `Breed` of the cat

We would like to store this information for each cat in a Relational DBMS - in this case, we use `Postgres`.

Given that we are all Docker nerds now, instead of installing and setting up Postgres on our machines locally, we will use Docker to set it up and tie it in with our server. To top it all off, we will access our Flask server and the database using a Docker Compose file for ease of use and faster processing.

## Step 0 - Creating a structure for our application
```
├── docker-compose.yml
├── init.db.sql
├── app
│ ├── app.py
│ ├── Dockerfile
│ └── requirements.txt
```

We will talk about all of the above files in a moment!

## Step 1 - Let's think about our database

Given that our task is very simple, we can just have a single `cat` table that has the followinga `attributes` or `columns`:

- `id`: Each cat/row will be assigned a unique Integer Id. We can start it from one and keep increasing it incrementally.
- `name`: A string for storing the name of the cat
- `color`: A string for storing the color of the cat
- `breed`: A string for storing the breed of the cat

Now, we would need to essentially create the table called `cat` in a database with the above columns and their types. When we are using Docker to run a database server, say MySQL or POSTGRES, Docker allows us to save an `initialization` file.

This file allows us to add some sql commands which are executed as soon as the database server is up and running in the docker container. We usually use this files to set up the database the way we want - in this case, we would like to create our cat table as soon as the database server is up and running.

[`init.db.sql`](./init.db.sql)

```
CREATE TABLE IF NOT EXISTS cat (
    id SERIAL PRIMARY KEY,
    name VARCHAR(80),
    color VARCHAR(80),
    breed VARCHAR(80)
);
```

The above file stores nothing but a basic command to create a table called `cat` with the attributes that we discussed about. We will see how we use this file once we get to setting up our containers via Docker Compose.

## Step 2 - Creating our Flask server

Time to start working on our Flask server. By now, we already are accustomes with the three files that we need to run a Flask server in docker - The `py` file that actually hosts the server code, the `Dockerfile` that allows us to create/build an image for the Flask code, `requirements.txt` file that is used by Docker to install all dependencies needed for our server within the container.

Let's go ahead and create the necessary files.

[`Dockerfile`](./app/Dockerfile)

```
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip3 install requirements.txt

COPY . .

CMD ["python3", "app.py"]
```

Pretty standard commands up there, most of what you have already covered and used in your Lab-5.

[`requirements.txt`](./app/requirements.txt)

```
flask
Flask-SQLAlchemy
psycopg2==2.9.3
```

We install `Flask`, `Flask-SQLAlchemy` which is the library that allows us to interact with Postgres through Flask while `psycopg2` is the actual adapter that helps in executing and processing commands.

Note: For people using M1/M2 Macbooks, you should use `psycopg2==2.9.3` in your requirements file. The other people can use `psycopg2-binary==2.9.1`.

Now, finally onto the `app.py` file.

[`app.py`](./app/requirements.txt)

```
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

# The `app.config` dictionary is used to configure various settings
# for the Flask app. Here, we specify the database URI and set the
# `SQLALCHEMY_TRACK_MODIFICATIONS` option to `False`, which tells
# SQLAlchemy not to track changes to database objects unless we
# explicitly tell it to do so.
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@db:5432/cats_db"
db = SQLAlchemy(app)

# Define a `Cat` model, which will map to a `cats` table in the database.
class Cat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    color = db.Column(db.String(80))
    breed = db.Column(db.String(80))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'breed': self.breed
        }

@app.route('/cats')
def get_cats():
    cats = Cat.query.all() # Queries all records in that model/table - SELECT *
    return jsonify([cat.to_dict() for cat in cats])


@app.route('/cats/<int:id>')
def get_cat(id):
    cat = Cat.query.filter_by(id=id).first() # filter_by allows us to add filters to our Queries - SELECT * FROM cat WHERE ....
    if cat:
        return jsonify(cat.to_dict())
    else:
        return jsonify({'error': 'Cat not found'})


@app.route('/cats', methods=['POST'])
def add_cat():
    data = request.get_json()
    new_cat = Cat(name=data['name'], color=data['color'], breed=data['breed'])
    db.session.add(new_cat) # Allows us to add/post new rows to the table
    try:
        db.session.commit() # Ensures that the data is actually written to the table - ACID properties anyone?
        return jsonify(new_cat.to_dict())
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': 'Cat already exists'})


@app.route('/cats/<int:id>', methods=['PUT'])
def update_cat(id):
    data = request.json
    cat = Cat.query.filter_by(id=id).first()
    if cat:
        cat.name = data.get('name', cat.name)
        cat.color = data.get('color', cat.color)
        cat.breed = data.get('breed', cat.breed)
        db.session.commit()
        return jsonify(cat.to_dict())
    else:
        return jsonify({'error': 'Cat not found'})


@app.route('/cats/<int:id>', methods=['DELETE'])
def delete_cat(id):
    cat = Cat.query.filter_by(id=id).first()
    if cat:
        db.session.delete(cat)
        db.session.commit()
        return jsonify({'message': 'Cat deleted'})
    else:
        return jsonify({'error': 'Cat not found'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
```

## Step 3 - Creating our Docker Compose

Now that we have our Flask server ready and the `init` file for our database ready, its time to start setting up our Docker so that we can run everything together

[`docker-compose.yml`](./docker-compose.yml)
```
version: '3'

services:
  db:
    image: postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: cats_db
    volumes:
      - ./init.db.sql:/docker-entrypoint-initdb.d/init.db.sql
    ports:
      - 5432:5432

  app:
    build: ./app
    ports:
      - 5050:5050
    depends_on:
      - db
```

The `app` component of the services is something that you are already familiar with. This helps us to build an image out of our Flask file and then create a container using that image.

In the `db` component, we are actually pulling an image from the Docker store online for `postgres`. This will allow Docker to ready its container and install Postgres on it. Note that by default, Docker runs Postgres on port `5432`.

We set up our config for the database like the username, password and what database we want to create and use using the `environments` key and we finally assign it the `init` file using the `volumes` key.