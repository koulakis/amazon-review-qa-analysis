
# coding: utf-8

# ## Loading and indexing the data for training

# In[2]:

# all_reviews = (spark
#     .read
#     .json('../../data/raw_data/reviews_Musical_Instruments_5.json.gz'))


# In[4]:

from pyspark.sql.functions import col, expr, udf, trim
from pyspark.sql.types import IntegerType
import re

remove_punctuation = udf(lambda line: re.sub('[^A-Za-z\s]', '', line))
make_binary = udf(lambda rating: 0 if rating in [1, 2] else 1, IntegerType())

reviews = all_reviews.withColumn('label', make_binary(col('overall')))


# In[5]:

from pyspark.ml.feature import StringIndexer
from pyspark.ml import Pipeline

indexing_pipeline = Pipeline(stages=[
    StringIndexer(inputCol="reviewerID", outputCol="reviewerIndex"),
    StringIndexer(inputCol="asin", outputCol="asinIndex")
])

indexer = indexing_pipeline.fit(reviews)
indexed_reviews = indexer.transform(reviews)


# In[6]:

train, _, test = [ chunk.cache() for chunk in indexed_reviews.randomSplit([.6, .2, .2], seed=1800009193L) ]


# ## Balancing data

# In[7]:

def multiply_dataset(dataset, n):
    return dataset if n <= 1 else dataset.union(multiply_dataset(dataset, n - 1))

reviews_good = train.filter('label == 1')
reviews_bad = train.filter('label == 0')

reviews_bad_multiplied = multiply_dataset(reviews_bad, reviews_good.count() / reviews_bad.count())

train_reviews = reviews_bad_multiplied.union(reviews_good)


# ## Evaluator

# In[8]:

from pyspark.ml.evaluation import RegressionEvaluator

evaluator = RegressionEvaluator(
    predictionCol='prediction', 
    labelCol='label')


# ## Benchmark: predict by distribution

# In[9]:

from pyspark.sql.functions import lit

average_rating = (train_reviews
    .groupBy()
    .avg('label')
    .collect()[0][0])

average_rating_prediction = test.withColumn('prediction', lit(average_rating))

average_rating_evaluation = evaluator.evaluate(average_rating_prediction)

print('The RMSE of always predicting {0} stars is {1}'.format(average_rating, average_rating_evaluation))


# ## Recommender system

# In[10]:

from pyspark.ml.recommendation import ALS

als = ALS(
        maxIter=15,
        regParam=0.1,
        userCol='reviewerIndex',
        itemCol='asinIndex',
        ratingCol='label',
        rank=24,        
        seed=1800009193L)


# ## Evaluating the model

# In[14]:

recommender_system = als.fit(train_reviews)


# In[15]:

predictions = recommender_system.transform(test)


# In[16]:

evaluation = evaluator.evaluate(predictions.filter(col('prediction') != float('nan')))

print('The RMSE of the recommender system is {0}'.format(evaluation))

