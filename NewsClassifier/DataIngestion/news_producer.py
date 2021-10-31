#!/usr/bin/python3
from kafka import KafkaProducer
import pandas as pd
import numpy as np
import json
import random
import requests
from queue import Queue
from threading import Thread
from time import time
from time import sleep
import os

KAFKA_BROKER = os.getenv('BROKER', 'localhost:9092')
KAFKA_TOPIC = 'news'

sleep(60)

try:
    producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)
except Exception as e:
    print(f'Error Connecting to Kafka --> {e}')


class ProducerWorker(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get work from queue
            source = self.queue.get()
            try:
                sendData(source)
            finally:
                self.queue.task_done()


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def sendData(source):
    if(source == 'rapidapi'):
        url = "https://free-news.p.rapidapi.com/v1/search"
        querystrings = {'sports': ['cricket', 'hockey'], 'politics': ['bjp', 'congress'], 'health': [
            'corona', 'vaccine'], 'religion': ['hindu', 'muslim', 'islam']}
        for key in querystrings:
            print(key)
            print(querystrings[key])
            # for q in querystrings[key]:
            #     querystring = {"q":q,"lang":"en"}
            #     headers = {
            #         'x-rapidapi-host': "free-news.p.rapidapi.com",
            #         'x-rapidapi-key': "554b1b9684msh5658af591a92b84p1c61aajsn39558bb41038"
            #         }
            #     response = requests.request("GET", url, headers=headers, params=querystring)

            #     total_pages = response.json().get('total_pages')
            #     sleep(1)

            #     for p in range(1, total_pages):
            #         querystring = {"q":q,"lang":"en", "page":p}
            #         response = requests.request("GET", url, headers=headers, params=querystring)
            #         # print(p)
            #         # print(response.json())
            #         data = response.json().get('articles')
            #         for d in data:
            #             if d['topic']=='news' :
            #                 d = {'title':d['title'],'date':str(d['published_date']),'summary':d['summary'],'category':key,'source':d['clean_url']}
            #             else :
            #                 d = {'title':d['title'],'date':str(d['published_date']),'summary':d['summary'],'category':d['topic'],'source':d['clean_url']}
            #             try:
            #                 print("sending...", str(d))
            #             except Exception as e:
            #                 pass
            #             producer.send(KAFKA_TOPIC, json.dumps(d,cls=NpEncoder).encode("utf-8"))
            #             #print('message sent to topic')
            #             sleep(random.randint(3,5))

            #         sleep(1)

    else:
        data = []
        with open('data/News_Category_Dataset_v2.json', mode='r', errors='ignore') as json_file:
            for dic in json_file:
                data.append(json.loads(dic))

        for d in data:
            d = {'title': d['headline'], 'date': str(
                d['date']), 'summary': d['short_description'], 'category': d['category'], 'source': d['link']}
            try:
                print("sending...", str(d))
            except Exception as e:
                pass
            producer.send(KAFKA_TOPIC, json.dumps(
                d, cls=NpEncoder).encode("utf-8"))
            #print('message sent to topic')
            sleep(random.randint(3, 5))


def main():
    sources = ['rapidapi', 'static']
    queue = Queue()
    for x in range(2):
        worker = ProducerWorker(queue)
        worker.daemon = True
        worker.start()
    for source in sources:
        queue.put((source))
    queue.join()


if __name__ == '__main__':
    main()
