#!/usr/bin/python3
from kafka import KafkaConsumer
import json
from pymongo import MongoClient
from time import sleep
import os

KAFKA_BROKER = os.getenv('BROKER', 'localhost:9092')
KAFKA_TOPIC = 'news'


def main():
    mongoUrlLocal = "mongodb://admin:password@localhost:27017"

    # use when starting application as docker container
    mongoUrlDocker = "mongodb://admin:password@mongodb:27017"

    db_name = 'news'
    collection_name = 'news_collection'

    mongo_client = MongoClient(mongoUrlDocker)
    mongo_db1 = mongo_client[db_name]
    mongo_collection1 = mongo_db1[collection_name]

    sleep(60)  # Topic creation taking time
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group')

    for data in consumer:
        print("consuming... ", data)
        mongo_collection1.insert_one(json.loads(data.value))
        # x = mongo_collection1.find()
        # print(x)


if __name__ == '__main__':
    main()
