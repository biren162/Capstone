## Terminal-1:

Step-1> Build and start Container

* docker-compose up --build

* To verify contents of news_collection under news DB, open localhost:8082 in browser.


## Terminal-2:

Step-2> To copy preprocessor pipeline

* docker cp milestone-2_preprocessor_1:/app/preprocessor ./models/.

* To verify the cleaned data, check preprocessor logs using "docker logs milestone-2_preprocessor_1"
