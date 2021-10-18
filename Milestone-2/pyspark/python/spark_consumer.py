import findspark
findspark.init()

import pandas as pd

import json
from pyspark import SparkContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.streaming import StreamingContext
from utils import predict_and_build_result

def create_df(d):
    keys = list(d.keys())
    values = list(d.values())
    df = pd.DataFrame(columns=keys)
    df.loc[0]=values
    #print(df)
    return df

def predict(d):
    df = create_df(d)
    result = predict_and_build_result(df)
    return result

sc = SparkContext(appName="HousePrice")
ssc = StreamingContext(sc, 60)

TOPIC = 'house'
KAFKA_BROKERS = 'kafka:9092'

print('creating stream...')

stream = KafkaUtils.createDirectStream(
                            ssc,
                            [TOPIC],
                            {"metadata.broker.list": KAFKA_BROKERS})
stream = stream.map(lambda x: json.loads(x[1]))

res = stream.map(lambda data: predict(data))

res.pprint()

ssc.start()
ssc.awaitTermination()