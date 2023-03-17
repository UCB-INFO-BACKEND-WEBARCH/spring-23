# Asynchronous Task Queues

## Intro to Async Queues

Whatever we have learnt till now in this course has revolved around synchronous execution of tasks. However, most of the real-world processes around us are actually asynchronous.
Think about you ordering food and the time it takes for it to arrive at your doorstep.

In the world of APIs too, a lot of processes are asynchronous. Whenever we execute a piece of code which takes some time, the execution will most likely be asynchronous.
Consider the following example:
You are building a Data Visualization platform where the flow is something like: 1. You upload a dataset 2. You select a few features and parameters 3. The platform creates a visualization for you and presents it as a dashboard
Sounds cool right?

But we know that datasets are big (especially in the age we live, data is available for chump change). So it is highly likely that the data upload will take some time. Moreover, once it is uploaded, it will take some time for the data to be processed for the platform to showcase relevant features/column names etc and then there will be more time required to actually create the visualization.

So what do we do when all these processes are taking place in the background? Do we stop the user from doing anything on the platform and make them see a loader for an hour? Doesn't sound right!

This is where Asynchronous Queus come in. Asynchronous Task Queues are essential tools in building scalable and efficient backend systems. They allow for the execution of long-running or resource-intensive tasks to be offloaded to a separate worker process or server, freeing up the main application thread to continue processing requests. This can greatly improve the responsiveness and throughput of the system.

Asynchoronous Queues are used to store and process tasks that will take up some time while the system can move on to doing other things rather than waiting for the previous process to finish executing. Once the task has finished executing, these queues usually have a `callback` functionality which notify that the processor that the task has been executed and then the processor can do what it was supposed to do with it.

Let's think about this through another example. When you go to a restaurant to order something, does the waiter/waitress stop by your table and wait while you look at the menu and decide what you want to eat? Not unless you have questions! They will go around and serve other tables while you decide. Once you have decided, you signal or call the waiter/waitress and convey your order. The waiter/waitress then gives your order into the kitchen, who again take time to cook the food. Once the food is cooked, the waiter/waitress is called by the kitchen and then they bring you your food.

The waiter/waitress in this case is like an Async Queue while you and all the other guests at the table are tasks which are executing asynchronously. The kitchen is the processor.

## So why do we actually need Async Queues?

There are three main reasons:

<ol>
<li> <b>Speed</b>: When we’re talking to a third party API we have to face reality; unless that third party is physically located next to our infrastructure, there’s going to be latency involved. All it would take is the addition of a few API calls and we could easily end up doubling or tripling our response time, leading to a sluggish site and unhappy users. However if we push these API calls into our queue instead, we can return a response to our users immediately while our queues take as long as they like to talk to the API.</li>
</br>
<li><b>Reliability</b>: We don’t live in a world of 100% uptime, services do go down, and when they do it’s important that our users aren’t the ones that suffer. If we were to make our API calls directly in the users requests we wouldn’t have any good options in the event of a failure. We could retry the call right away in the hope that it was just a momentary glitch, but more than likely we’ll either have to show the user an error, or silently discard whatever we were trying to do. Queues neatly get around this problem since they can happily continue retrying over and over in the background, and all the while our users never need to know anything is wrong.</li>
</br>
<li><b>Scalability</b>. If we had a surge in requests that involved something CPU intensive like resizing images, we might have a problem if all of our apps were responsible for this. Not only would the increased CPU load slow down other image resize requests, it could very well slow down requests across the entire site. What we need to do is isolate this workload from the user’s experience, so that it doesn’t matter if it happens quickly or slowly. This is where queues shine. Even if our queues become overloaded, the rest of the site will remain responsive.</li>
</ol>

## How do they work?

There are several components involved in setting up and using an Asynchronous Task Queue:

1. <b>Task Queue</b>: This is the main component that manages the task queue and worker processes. It receives tasks from the application and sends them to the worker processes for execution.

2. <b>Worker Process</b>: This is a separate process that executes the tasks in the background. It receives tasks from the Task Queue and executes them asynchronously. Task queues allow us to offload jobs to another worker process, meaning we can return something to the user immediately while the job gets placed in a queue and processed at a later time (depending on how many tasks are currently in the queue, it could start at a later time or immediately). We can also have more than one worker to parallely execute tasks.

3. <b>Message Broker</b>: This is a service that acts as an intermediary between the Task Queue and the Worker Processes. It receives messages from the Task Queue and delivers them to the Worker Processes.

We also have `producers` and `consumers` in the periphery that interact with the queue.

Using the restaurant example again, we can map all the participants as following:

1. Kitchen -> Producer
2. Customers -> Consumers
3. Restaurant Manager -> Message Broker
4. Waiter -> Workers/Task Queues

## How will we use an Async Queue?

To use Asynchronous Task Queues in a Flask, Docker, and Postgres stack, we need to:

1. <u>Install Redis</u>: Redis is a popular in-memory data store that can be used as a Message Broker for Asynchronous Task Queues. We need to install Redis on our system and start the Redis server.

2. <u>Install Celery</u>: Celery is a distributed task queue that supports multiple message brokers, including Redis. We need to install Celery and configure it to use Redis as the message broker.

3. <u>Create Tasks</u>: We need to define the tasks that we want to execute asynchronously. These tasks can be simple functions that perform a specific task or complex workflows that involve multiple steps.

4. <u>Queue Tasks</u>: We need to enqueue the tasks for execution in the Task Queue. This can be done using the Celery API, which allows us to add tasks to the queue and track their status.

5. <u>Execute Tasks</u>: The Worker Processes will pick up the tasks from the Task Queue and execute them in the background. The results of the tasks can be retrieved using the Celery API.

## Other relevant services

For the `task queue` we can also use [`RQ`](https://python-rq.org/) instead of Celery.

Instead of Redis, we can also use `RabbitMQ`, `Amazon SQS` or even `Apache Kafka`.

## Demo

We will set up a basic HTML form that takes in a user's name and an email. This is essentially a signup form for a newsletter.

We would then let this form submission hit a Flask endpoint which will store it into a Postgres table. We will have another endpoint which accept some HTML data and then send that out as email using Sendgrid to everyone in the table.

Let's go step-by-step for the demo!

### Setting up our HTML file

We will just quickly set up an [HTML](./demo/app/template/index.html) file that has an HTML form and hits a POST `/register` endpoint on our Flask server.

### Starting with a basic Flask server

Not let's set up the Flask server. To begin with, let's just create a POST endpoint that expects the name and email and adds it to a Postgres database.

```
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Registration(db.Model):
    email = db.Column(db.String(120), primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<Registration %r>' % self.email


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/register', methods=["POST"])
def register():
    email = request.form['email']
    name = request.form['name']
    new_registration = Registration(email=email, name=name)
    db.session.add(new_registration)
    db.session.commit()
    return 'Registration successful!'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
```

We are doing things that we have already learnt and done till now. We have an index endpoint that served our HTML file and we have an endpoint to take in the two input data points and add it to our Postgres table called `registration` using the ORM model.

### Running everything we have so far using Docker
Now that we have our HTML file and the Flask server, its time to spin up a Postgres server and run everything together using Docker.

We add the [`Dockerfile`](./demo/app/Dockerfile) for our Flask server and the [`requirements.txt`](./demo/app/requirements.txt) file. We then add our [`Docker Compose`](./demo/docker-compose.yml) yaml and the database [`init`](./demo/init.db.sql) file. All of it is the same as last week.

Let's try running everything to see if the data is getting registered into Postgres.

Now, onto the tougher part.

### Creating endpoint for sending emails
We create another POST endpoint - `/send` that takes in the email subject and body from a JSON request and then sends an email to everyone in our database.

However, now that we are trying to call an external API, it is best practice to make this an Async call as you don't know how long that will take.

So, our endpoint handler will essentially handover the execution of the email sending to `Celery`, which is our task queue.

Here is our updated Flask [server](./demo/app/server.py)
```
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from worker import sendEmailTask

app = Flask(__name__, template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Registration(db.Model):
    email = db.Column(db.String(120), primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<Registration %r>' % self.email


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/register', methods=["POST"])
def register():
    email = request.get_json()['email']
    name = request.get_json()['name']
    new_registration = Registration(email=email, name=name)
    db.session.add(new_registration)
    db.session.commit()
    return 'Registration successful!'


@app.route('/send', methods=["POST"])
def sendEmails():
    data = request.get_json()
    emailBody = data['body']
    emailSubject = data['subject']

    registrations = Registration.query.all()
    emails = [registration.email for registration in registrations]
    taskIDs = []
    for email in emails:
        emailAsyncTask = sendEmailTask.delay(email, emailBody, emailSubject)
        taskIDs.append(emailAsyncTask.id)
    return {"tasks": taskIDs}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
```

So what's changed?

1. We import the Worker function that actually sends the emails from another container so that our Python file can call that container.
2. We create a new endpoint that accepts a JSON request body with the required data
3. We get all emails from the database and pass that to the worker function alongside the required data.

Let's look more closely at the sendEmail handler.

```
# Import for sendEmailTask function from the worker container
from worker import sendEmailTask 
...

def sendEmails():
    data = request.get_json()
    emailBody = data['body']
    emailSubject = data['subject']

    registrations = Registration.query.all()
    emails = [registration.email for registration in registrations]
    taskIDs = []
    for email in emails:
        # The delay function allows us to send a assign a task to Celery to be executed async
        # We just pass on the three paramters that that function takes
        emailAsyncTask = sendEmailTask.delay(email, emailBody, emailSubject)
        taskIDs.append(emailAsyncTask.id)
    return {"tasks": taskIDs}
```

### Setting up our Worker
Now that we have our server all set up, let's create the worker that actually executes the task

[worker.py](./demo/worker/worker.py)
```
import os
from celery import Celery
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Getting the required environment variables
broker_url = os.environ.get("CELERY_BROKER_URL"),
res_backend = os.environ.get("CELERY_RESULT_BACKEND")

# Connecting to Celery
celery_app = Celery(name='worker',
                    broker=broker_url,
                    result_backend=res_backend)

# Creating the definition for a celery task
@celery_app.task
def sendEmailTask(email, emailBody, emailSubject):
    try:
        # Sending email via Sendgrid
        message = Mail(
            from_email=os.environ.get('SENDGRID_FROM_EMAIL'),
            to_emails=email,
            subject=emailSubject,
            html_content=emailBody
        )
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        return response
    except Exception as e:
        print(e)
        return str(e)
```

### Dockerfile to run our worker

[Dockerfile](./demo/worker/Dockerfile)

```
FROM python:3.9-alpine
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["celery"]
CMD ["-A", "worker.celery_app", "worker"]
```

### Updating our Docker Compose file to tie it up together

[docker-compose.yaml](./demo/docker-compose.yml)
```
version: "3"

services:
  db:
    image: postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: users
    volumes:
      - ./init.db.sql:/docker-entrypoint-initdb.d/init.db.sql
    ports:
      - 5432:5432
```
The database remains the same!

```
  worker:
    build: ./worker
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - SENDGRID_FROM_EMAIL=rishabhmthakur2@gmail.com
      - SENDGRID_API_KEY=***
      - CELERY_RESULT_BACKEND=db+postgresql://postgres:postgres@db:5432/users
    volumes:
      - ./worker/worker.py:/app/worker.py
```
We add a `worker` container that uses the worker folder to build an image and run Celery and the worker. We add the necessary environment files needed for the same.

```
  redis:
    image: redis
    ports:
      - "6379:6379"
```
We set up a redis broker at the default port mapping and by using the Docker image.

```
  app:
    build: ./app
    volumes:
      - ./worker/worker.py:/app/worker.py
    ports:
      - 5050:5050
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - SENDGRID_FROM_EMAIL=rishabhmthakur2@gmail.com
      - SENDGRID_API_KEY=***
      - CELERY_RESULT_BACKEND=db+postgresql://postgres:postgres@db:5432/users
    depends_on:
      - db
      - redis
      - worker
```
We add the shared volume/worker file to our app service and also other relevant environment variables. We also make this app service dependent on other services.

```
  job_viewer:
    image: mher/flower
    environment:
      - CELERY_BROKER_URL=redis://redis:6379
      - FLOWER_PORT=8888
    ports:
      - 8888:8888
    depends_on:
      - redis

```
We add a Job viewer using the Docker image that will allow us to monitor our jobs and workers using a GUI.