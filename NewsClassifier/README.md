## Terminal-1:

Step-1> Build and start Container

* docker-compose up --build

* To verify contents of news_collection under news DB, open localhost:8082 in browser.


## Terminal-2:

Step-2> To copy preprocessor pipeline to local registery

* docker cp newsclassifier_preprocessor_trainer_1:/app/preprocessor ./models/.

* To verify the cleaned data, check preprocessor logs using "docker logs newsclassifier_preprocessor_trainer_1"

## Model training:
* To verify random forest(pyspark) training accuracy, check trainer logs using "docker logs newsclassifier_preprocessor_trainer_1"
* To train Bert model, run notebook news_classification_bert.ipynb

## UI: 
* To access News Classifier UI, open localhost:8888 in browser

## News Category prediction:
  	- Update docker memory resource allocation = 4 GB
  	- Wait for prediction service startup to complete (docker-compose logs --follow predictor)
  	- Open localhost:8888 in browser, enter news article summary and wait for some seconds to get predicted news category.
