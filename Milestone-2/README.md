Terminal-1:

docker-compose up --build

In browser open localhost:8082
Verify contents of news_collection under news DB

Terminal-2:

docker-compose run preprocessor bash

cd python

spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.3.5 ./news_preprocessor.py


