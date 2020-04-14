# Truck Simulator 2020

- [Installation and basic usage](#installation-and-basic-usage)
- [Structure and contents](#structure-and-contents)
  * [Back-end](#back-end)
  * [Front-End](#front-end)
  * [Data producer](#data-producer)
  * [Data consumer](#data-consumer)
  * [Database](#database)

## Installation and basic usage

From the main directory run `docker-compose build`. To launch the services run the `run_docker.sh` bash script. Please note you should first make it executable running `chmod +x run_docker.sh` and might need to specify the `bash` command if you are not running a bash terminal (`bash run_docker.sh`).

You can specify the number of trucks to run the simulation : `run_docker.sh 5` will run the simulation for 5 trucks. If you do not specify the simulation defaults to 4 trucks.

## Structure and contents

### Back-end

The back-end files are found in the **back** folder.
This is a Flask back-end running on Python 3.7, used libraries can be found under requirements.txt.

### Front-End

The front-end files are found in the **client** folder. This is a Vue.js front-end built for production using nginx. 

### Data producer

The files for the data producer service are found under **data_simulation/data_publisher**.

The service is built on python 3.7, used libraries can be found under requirements.txt. 

The service communicates directly with a RabbitMq instance using the [Pika](https://pika.com/) library. The producer uses threads to run each truck and sends message into a RabbitMq queue, waiting for the consumer service to read them. 

The service also has write actions in a postgresql database for truck and driver creation. 

The service is ran using main.py, by default 4 trucks are ran if no options are specified. 


### Data consumer

The files for the data producer service are found under **data_simulation/data_consumer**.

The service is built on python 3.7, used libraries can be found under requirements.txt. 

The service acts as a consumer awaiting messages from the producer service. It communicates both with a RabbitMq instance using the [Pika](https://pika.com/) library and with a postgresql database using SQLalchemy on Python. 

### Database

Various files on database initialisation can be found under the **docker** folder.

<!-- ### Used Libraries :

- [Pika](https://pika.com/) (RabbitMQ)

### Run database
- `docker-compose up` -->
