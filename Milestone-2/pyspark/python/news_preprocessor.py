#!/usr/bin/python3
import sys
from pyspark.sql import SQLContext, SparkSession
from pyspark import SparkContext, SparkConf
from pyspark.ml.feature import Tokenizer, StopWordsRemover, HashingTF, IDF, StringIndexer
from pyspark.ml import Pipeline
import numpy
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

sparkConf = SparkConf().setMaster("local").setAppName("MongoSparkConnectorTour").set("spark.app.id", "MongoSparkConnectorTour")

#If executed via pyspark, sc is already instantiated
sc = SparkContext(conf=sparkConf)
sqlContext = SQLContext(sc)

# create and load dataframe from MongoDB URI
df = sqlContext.read.format("com.mongodb.spark.sql.DefaultSource")\
        .option("spark.mongodb.input.uri", "mongodb://admin:password@mongodb:27017/news.news_collection?authSource=admin")\
                    .load()

# print data frame schema
df.printSchema()

# print first dataframe row
# df.first()

# convert dataframe to rdd 
# rdd = df.rdd 
# rdd.first()

print('cleaning start')

print(df.columns)

stopwords = stopwords.words('english')
tokenizer = Tokenizer(inputCol="summary", outputCol="words")
stopwordsRemover = StopWordsRemover(inputCol="words", outputCol="filtered_data").setStopWords(stopwords)
hashingTF = HashingTF(inputCol="filtered_data", outputCol="tf", numFeatures=10000)
idf = IDF(inputCol="tf", outputCol="idf", minDocFreq=5)
labelAnnotator = StringIndexer(inputCol = "category", outputCol = "label")
preprocessorPipeline = Pipeline(stages=[tokenizer, stopwordsRemover, hashingTF, idf, labelAnnotator])
preprocessorPipelineFit = preprocessorPipeline.fit(df)

#preprocessorPipelineFit.save('preprocessor')
#preprocessor = Pipeline.load("preprocessor")

cleaned_df = preprocessorPipelineFit.transform(df)
#cleaned_df = preprocessor.transform(df)

print('cleaning done')
print(cleaned_df.columns)
print(cleaned_df.show(5))



print("Done")
sys.exit(0)