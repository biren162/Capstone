## NewsClassifier

#### Services in NewsClassifier

* DataIngestion: Data sources to mongo db through kafka queue

* Preprocessing_And_Training: mongo db to spark dataframe, data cleansing and training using pyspark (Track models using mlflow)

* Prediction: Predict using the saved trained model 

#### How to run application

* Follow the instructions in NewsClassifier/README.md