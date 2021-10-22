#!/usr/bin/python3
import sys
from time import sleep
from pyspark.sql import SQLContext, SparkSession
from pyspark import SparkContext, SparkConf
from pyspark.ml.feature import Tokenizer, StopWordsRemover, HashingTF, IDF, StringIndexer
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
import numpy
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

sleep(70)

sparkConf = SparkConf().setMaster("local").setAppName("MongoSparkConnectorTour").set("spark.app.id", "MongoSparkConnectorTour")

#If executed via pyspark, sc is already instantiated
sc = SparkContext(conf=sparkConf)
sqlContext = SQLContext(sc)

# create and load dataframe from MongoDB URI
df = sqlContext.read.format("com.mongodb.spark.sql.DefaultSource")\
        .option("spark.mongodb.input.uri", "mongodb://admin:password@mongodb:27017/news.news_collection?authSource=admin")\
                    .load()

# print data frame schema
print('Schema')
df.printSchema()

print('Columns in Existing Dataframe: ', df.columns)
print('Data cleansing starts...')

# Feature Selection
df = df['summary','category']

stopwords = stopwords.words('english')
tokenizer = Tokenizer(inputCol="summary", outputCol="words")
stopwordsRemover = StopWordsRemover(inputCol="words", outputCol="filtered_data").setStopWords(stopwords)
hashingTF = HashingTF(inputCol="filtered_data", outputCol="tf", numFeatures=10000)
idf = IDF(inputCol="tf", outputCol="idf", minDocFreq=5)
labelAnnotator = StringIndexer(inputCol = "category", outputCol = "label")
assembler = VectorAssembler(inputCols=['tf','idf'], outputCol='features')
preprocessorPipeline = Pipeline(stages=[tokenizer, stopwordsRemover, hashingTF, idf, labelAnnotator, assembler])
preprocessorPipelineFit = preprocessorPipeline.fit(df)

preprocessorPipelineFit.save('preprocessor')

preprocessor = PipelineModel.load("preprocessor")

#cleaned_df = preprocessorPipelineFit.transform(df)
# let's train on few records only
df = df.limit(100)
cleaned_df = preprocessor.transform(df)

print('Data cleansing done!!')

print('Columns after data cleansing: ',cleaned_df.columns)

# cleaned_df = cleaned_df['summary', 'category', 'tf', 'idf', 'label']

print('Schema after data cleansing')
cleaned_df.printSchema()
print(cleaned_df.show(5))

print("Done")

#Data Partition

(trainingData, testData) = cleaned_df.randomSplit([0.7, 0.3], seed = 100)


rf = RandomForestClassifier(labelCol='label',
                            featuresCol='features')
print('========================stating the training....=========== #records:',df.count())
lrModel = rf.fit(trainingData)
predictions = lrModel.transform(testData)

evaluator = MulticlassClassificationEvaluator(predictionCol="prediction")
print('accuracy------------------------------------------------------------------:',evaluator.evaluate(predictions))

print('response----------------------------------------------------------:')
print(predictions.filter(predictions['prediction'] == 0) \
    .select("summary","category","probability","label","prediction") \
    .orderBy("probability", ascending=False) \
    .show(n = 10, truncate = 30))
sys.exit(0)



# import sparknlp
#
# spark = sparknlp.start()
#
# from sparknlp.base import *
# from sparknlp.annotator import *
#
#
# documentAssembler = DocumentAssembler()\
#     .setInputCol("summary")\
#     .setOutputCol("document")
#
# print('finally spark nlp is working...')
#
# documentAssembler = DocumentAssembler()\
#     .setInputCol("summary")\
#     .setOutputCol("document")
#
# tokenizer = Tokenizer() \
#     .setInputCols(["document"]) \
#     .setOutputCol("token")
#
# stemmer = Stemmer() \
#     .setInputCols(["token"]) \
#     .setOutputCol("stem")
#
# bert_embeddings = BertEmbeddings.pretrained('bert_base_uncased')\
#           .setInputCols(["document", "token"])\
#           .setOutputCol("embeddings")
#
# nlpPipeline = Pipeline(stages=[
#     documentAssembler,
#     tokenizer,
#     bert_embeddings
#  ])
#
# empty_df = spark.createDataFrame([['']]).toDF("text")
#
# pipelineModel = nlpPipeline.fit(empty_df)
#
# result = pipelineModel.transform(df.limit(10))
#
# print(result.show(5))