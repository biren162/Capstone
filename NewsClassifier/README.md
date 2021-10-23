## Terminal-1:

Step-1> Build and start Container

* docker-compose up --build

* To verify contents of news_collection under news DB, open localhost:8082 in browser.


## Terminal-2:

Step-2> To copy preprocessor pipeline

* docker cp milestone-2_preprocessor_1:/app/preprocessor ./models/.

* To verify the cleaned data, check preprocessor logs using "docker logs milestone-2_preprocessor_1"


# Steps to run notebook in local
open anaconda prompt
type pyspark

# UI: 
localhost:8888   (windows)

# Model training:
 run notebook final_news_classification_bert.ipynb

# Model prediction:
  	- Update docker memory resource allocation = 4 GB
  	- Prediction service takes few seconds to give output
