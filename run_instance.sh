#!/bin/bash

docker-compose up -d
python data_publisher/main.py & python data_consumer/consumer.py