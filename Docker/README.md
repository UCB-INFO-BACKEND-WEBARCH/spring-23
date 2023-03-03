# Virtual Machines, Containers and Docker

## Virtualization and Virtual Machines

### What is a virtual machine?

Virtualization is the creation of a virtual version of something, such as a server, operating system, storage device, or network resources. Virtualization enables multiple operating systems to run on a single physical machine, allowing for increased flexibility and efficiency.

Virtual machines (VMs) are a form of virtualization that allow for the creation of multiple isolated environments on a single physical machine. Each VM runs its own operating system and behaves like a separate physical machine. This allows for greater flexibility and isolation compared to running multiple applications on a single operating system.

### How does it work?

Virtual machines (VMs) are created using virtualization technology that allows multiple operating systems to run on a single physical machine. A hypervisor or virtual machine monitor (VMM) sits between the hardware and the virtual machine, allocating the machine's resources (such as CPU, memory, and storage) to each VM as needed.

When a new VM is created, a virtual hardware environment is set up for it, including virtual CPUs, virtual memory, virtual storage devices, and virtual network interfaces. Each VM runs its own operating system and applications, just like a physical machine, and is completely isolated from other VMs running on the same physical machine.

### Pros of using a VM

- <b>Isolation</b>: Each VM is isolated from the others, providing greater security and reliability.
- <b>Flexibility</b>: VMs can run different operating systems and applications on a single physical machine, providing greater flexibility in resource utilization.
- <b>Cost savings</b>: VMs can reduce hardware costs by allowing multiple virtual machines to run on a single physical machine.

### But it can't all be good right?

- <b>Overhead</b>: VMs require additional resources to run, such as memory and CPU.
- <b>Complexity</b>: VMs can be more complex to set up and manage than running multiple applications on a single operating system.

### Some useful links

- [How virtual machines work](https://www.ibm.com/topics/virtual-machines)

## Containers

### What is a container?

Containers are a lightweight form of virtualization that allow for the creation of isolated environments for applications to run in. Unlike virtual machines, containers share the same kernel as the host operating system, making them much more lightweight and efficient.

Containers allow for applications to be packaged with all of their dependencies and configuration files, making them highly portable and easy to deploy across different environments.

### How do they work?

Containers are similar to VMs in that they allow multiple applications to run on a single physical machine, but they use a different approach to virtualization. Containers use the operating system kernel of the host machine to isolate applications from each other and provide them with their own runtime environment.

A container consists of an application and all its dependencies, packaged into a single, lightweight executable file. When a container is started, the host machine creates a separate namespace for it, including a separate file system, network interface, and process tree. The container runs within this namespace, completely isolated from other containers and the host machine.

### What's good about them?

- <b>Isolation</b>: Containers provide a level of isolation between applications, making them more secure and reliable.
- <b>Portability</b>: Containers can be easily moved between different environments, making them highly portable.
- <b>Efficiency</b>: Containers are much more lightweight than virtual machines, requiring less overhead to run..

### Again, where's the dirt?

- <b>Limited isolation</b>: Containers share the same kernel as the host operating system, which can lead to security vulnerabilities.
- <b>Complexity</b>: Containers can be complex to set up and manage, especially when dealing with large-scale deployments.

### Some useful links

- [Understanding Containers](https://www.redhat.com/en/topics/containers)

## To sum it all up - VMs vs Containers

### Virtual Machines:

- Fully isolated instances of an operating system and associated applications.
- Each VM runs on a hypervisor that emulates the underlying hardware.
- Each VM requires its own operating system, resulting in higher resource requirements and slower startup times.
- Can run multiple operating systems and applications on a single physical host.
- Can be used to test different operating systems or software configurations, or to provide multiple isolated environments for applications.

### Containers:

- Lightweight, isolated instances of an application running on the same operating system.
- Containers share the host operating system's kernel, eliminating the need for emulated hardware and reducing resource requirements.
- Can be started and stopped quickly, making them ideal for scaling applications up or down.
- Can be used to isolate individual services within a larger application, or to create a consistent environment for developing and testing applications.
- Can be deployed in a container orchestration system, such as Kubernetes, for automatic scaling and management.

Overall, virtual machines are more suitable for environments where complete isolation is required, or for running multiple operating systems and applications on the same physical host. Containers, on the other hand, are better suited for scaling applications, isolating individual services within a larger application, or providing a consistent environment for application development and testing.

## Docker

Docker is a platform for building, shipping, and running applications in containers. Docker provides a simple and efficient way to package applications and their dependencies, making them highly portable and easy to deploy.

Docker allows for the creation of Docker images, which are portable snapshots of an application and its dependencies. Docker images can be easily shared and deployed across different environments, making them highly scalable and flexible.

Moreover, Docker containers are lightweight and portable, making it easy to move applications between different machines or cloud environments.

### How does it work?

Docker works by using a client-server architecture. The Docker client communicates with the Docker daemon, which is responsible for building, running, and managing containers. Docker uses a layered file system, which allows for efficient sharing of files between containers.

### Some important commands

- `docker build`: This command is used to build an image from a Dockerfile.

- `docker run`: This command is used to start a container.

- `docker ps`: This command is used to list running containers.

- `docker stop`: This command is used to stop a running container.

- `docker rm`: This command is used to remove a container.

- `docker images`: This command is used to list the available Docker images.

- `docker pull`: This command is used to download a Docker image from a registry.

## Setting up your Flask server within a Docker

Here comes the fun part!

We have already worked on multiple Flask servers. One basic server is mentioned below:

```
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
```

Let's save this file as `app.py`. This simple Flask server creates a route for the root URL and returns a "Hello, World!" message.

To run this Flask application using Docker, you'll need to follow these steps:

1. Create a `requirements` file
   We need our dependencies like Flask, json or anything else that your code would like to install, import and use to be installed and delivered with the image, so we need to put them in the `requirements.txt` file

For now, let's say we only need Flask. So our file would look something like this:

```
Flask
```

2. Create a `Dockerfile` in your application's root directory. A `Dockerfile` contains a set of instructions describing our desired image and allow its automatic build.

```
# Use an official Python runtime as an image
FROM python:3.8

# The EXPOSE instruction indicates the ports on which a container
# will listen for connections
# Since Flask apps listen to port 5000 by default, we expose it
EXPOSE 8000

# Sets the working directory for following COPY and CMD instructions
# Notice we haven’t created a directory by this name - this instruction
# creates a directory with this name if it doesn’t exist
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app
RUN pip install -r requirements.txt

# Run app.py when the container launches
COPY app.py /app
CMD python app.py
```

This `Dockerfile` specifies the base Python image to use, installs the dependencies specified in requirements.txt, copies the application code into the container, exposes port 5000 (which is the port that the Flask server is running on), and sets the command to run the Flask server.

3. Create an `image` using the Dockerfile

`docker build -t my-flask-app .`

4. Run the Docker container

`docker run -p 8000:5050 my-flask-app`

This command starts a Docker container using the `my-flask-app` image and maps port 8000 on the host to port 5000 in the container.

When you run a container using the docker run command with the -p flag, you're specifying a port mapping between the host machine and the container. The syntax for this flag is -p `host_port `:`container_port`.

5. You can stop and delete the container using its id

`docker stop <container-id>`

`docker rm <container-id>`

## Docker Compose

Docker Compose is a tool for defining and running multi-container Docker applications. With Docker Compose, you can define the services that make up your application in a `docker-compose.yml` file, and then use the docker-compose command to start and stop your application.

Docker Compose allows you to define the configuration for your application in a declarative way, making it easy to maintain and scale. You can define the services, volumes, networks, and other configuration options for your application in a single file, and then start and stop your application with a single command.

### Why and Where to use Docker Compose

Docker Compose is useful when you have multiple services that make up your application, and you want to manage them as a single entity. It allows you to define the dependencies between your services and configure them in a consistent way.

Docker Compose can be used in a variety of scenarios, such as:

- <b>Development</b>: Docker Compose can be used to define the development environment for your application, including databases, cache servers, and other services that your application depends on.

- <b>Testing</b>: Docker Compose can be used to define the test environment for your application, including test databases and other services that your tests depend on.

- <b>Production</b>: Docker Compose can be used to define the production environment for your application, including load balancers, caching layers, and other services that your application depends on.

### Using Docker Compose to run two flask servers

Our folder structure would look something like this:

```
├── docker-compose.yml
├── flask1
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
└── flask2
    ├── app.py
    ├── Dockerfile
    └── requirements.txt
```

In the flask1 and flask2 folders, you'll have a similar structure:

```
Copy code
├── app.py
└── requirements.txt
```

Here's the `app.py` code for `flask1`:

```
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World! This is Flask 1.'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
```

And here's the `app.py` code for `flask2`:

```
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World! This is Flask 2.'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
```

Here's the requirements.txt file for both flask1 and flask2:

```
Flask==2.1.4
```

Here's the Dockerfile for both:

```
FROM python:3.8

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

CMD python3 ./app.py
```

### Docker Compose YAML

he Docker Compose YAML file is a configuration file used to define and manage multiple Docker containers as a single application. It is used to specify the services, networks, volumes, and environment variables required to run the application.

The Docker Compose YAML file defines each service in a separate section, with its own set of parameters and configurations. These services can be built from a Dockerfile or use a pre-built Docker image. The YAML file also defines the networks and volumes that the services will use to communicate with each other and store data.

By using a Docker Compose YAML file, developers can easily spin up and manage multiple containers with a single command, simplifying the deployment and management of complex applications. It also provides a unified and consistent way of defining the application stack, making it easier to share and collaborate on application configurations.

```
version: '3'
services:
  flask1:
    build: ./flask1
    container_name: "Server 1"
    ports:
      - "8000:5050"
  flask2:
    build: ./flask2
    container_name: "Server 2"
    ports:
      - "8001:5050"
```

We are using two services, both of them being different flask servers.

- `build`: specifies the directory which contains the Dockerfile containing the instructions for building this service
- `container name`: specifies the name of the container when it is finally deployed
- ports: mapping of : ports. So here, our POSTMAN will call the docker container (our application host) at port 8000 but the container in itself is running the Flask app on 5050.

To start the two Flask containers using Docker Compose, we can run the following command: `docker-compose up`

This will start both Flask services in the foreground, and we can see their logs in the terminal. If we want to run the services in the background, we can use the -d flag: `docker-compose up -d`

To stop the containers, we can use the following command: `docker-compose down`
