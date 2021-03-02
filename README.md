# Mongo App

This repository implements a simple app which allows the user to save simple
task on a NoSQL database (MongoDb in this case). These get automatically
executed and the results are also added to the entry task on the DB.

## Requirements
The main requirement is having Docker already installed on the system.

## Usage
The first step is to build the docker image defined on the Dockerfile:

> docker build -t mongo_app:last .

This will build a Docker image based on ubuntu:18.04 image and install MongoDB
on it.
After this step is completed, the docker image can be started with:

> docker run -it -p 11000:11000 -v $PWD:/usr/src/mongo_app/ mongo_app:last

This will launch the docker image, install the python requirements listed on
the requirements.txt file, start mongodb and launch the Flask app on port
11000 (which has already been mapped to the local port 11000)

## Testing

The application can be tested both manually or automatically.

### Manual testing

In order to test both endpoints you can use a third party app like Postman
or a terminal application like curl.
In order to create a new entry on the database, the following command can be
used:

> curl -X POST -H "Content-Type:application/json" -d '{"cmd": "ls"}' http://0.0.0.0:11000/new_task

The output should look like the following:

> {"id": entry_id}

In order to see the output results from the task the following command can be
executed:

> curl -X GET http://0.0.0.0:11000/get_output/<entry_id>

The output should look like the following:

> {"output": output}

### Automated testing

A simple testcase has been included on the testcases folder. This can be run
using pytest.
There are two options:

- Installing pytest on your local machine and running the testcase:

> pip3 install pytest==3.10.1

> python3 -m pytest

- Running it directly inside the docker:

> docker ps # Get the docker id from this command

> docker exec <docker_id> python3 -m pytest
