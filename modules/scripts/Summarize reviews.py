
# coding: utf-8

# # Summarize the reviews

# In[1]:

all_reviews = (spark
    .read
    .json('../../data/raw_data/reviews_Home_and_Kitchen_5.json.gz'))


# In[3]:

from pyspark.sql.functions import col, expr, udf, trim
from pyspark.sql.types import IntegerType
import re

remove_punctuation = udf(lambda line: re.sub('[^A-Za-z\s]', '', line))
make_binary = udf(lambda rating: 0 if rating in [1, 2] else 1, IntegerType())

reviews = (all_reviews
    .na.fill({ 'reviewerName': 'Unknown' })
    .filter(col('overall').isin([1, 2, 5]))
    .withColumn('label', make_binary(col('overall')))
    .select(col('label').cast('int'), remove_punctuation('summary').alias('summary'))
    .filter(trim(col('summary')) != ''))


# ## Splitting data and balancing skewness

# In[4]:

train, test = reviews.randomSplit([.8, .2], seed=5436L)


# In[5]:

def multiply_dataset(dataset, n):
    return dataset if n <= 1 else dataset.union(multiply_dataset(dataset, n - 1))


# In[6]:

reviews_good = train.filter('label == 1')
reviews_bad = train.filter('label == 0')

reviews_bad_multiplied = multiply_dataset(reviews_bad, reviews_good.count() / reviews_bad.count())


train_reviews = reviews_bad_multiplied.union(reviews_good)


# ## Benchmark: predict by distribution

# In[13]:

accuracy = reviews_good.count() / float(train.count())
print('Always predicting 5 stars accuracy: {0}'.format(accuracy))


# ## Learning pipeline

# In[8]:

from pyspark.ml.feature import Tokenizer, HashingTF, IDF, StopWordsRemover
from pyspark.ml.pipeline import Pipeline
from pyspark.ml.classification import LogisticRegression

tokenizer = Tokenizer(inputCol='summary', outputCol='words')

pipeline = Pipeline(stages=[
    tokenizer, 
    StopWordsRemover(inputCol='words', outputCol='filtered_words'),
    HashingTF(inputCol='filtered_words', outputCol='rawFeatures', numFeatures=120000),
    IDF(inputCol='rawFeatures', outputCol='features'),
    LogisticRegression(regParam=.3, elasticNetParam=.01)
])


# ## Testing the model accuracy

# In[9]:

model = pipeline.fit(train_reviews)


# In[10]:

from pyspark.ml.evaluation import BinaryClassificationEvaluator

prediction = model.transform(test)
BinaryClassificationEvaluator().evaluate(prediction)


# ## Using model to extract the most predictive words

# In[11]:

from pyspark.sql.functions import explode
import pyspark.sql.functions as F
from pyspark.sql.types import FloatType

words = (tokenizer
    .transform(reviews)
    .select(explode(col('words')).alias('summary')))

predictors = (model
    .transform(words)
    .select(col('summary').alias('word'), 'probability'))

first = udf(lambda x: x[0].item(), FloatType())
second = udf(lambda x: x[1].item(), FloatType())

predictive_words = (predictors
   .select(
       'word', 
       second(col('probability')).alias('positive'), 
       first(col('probability')).alias('negative'))
   .groupBy('word')
   .agg(
       F.max('positive').alias('positive'),
       F.max('negative').alias('negative')))

positive_predictive_words = (predictive_words
    .select(col('word').alias('positive_word'), col('positive').alias('pos_prob'))
    .sort('pos_prob', ascending=False))

negative_predictive_words = (predictive_words
    .select(col('word').alias('negative_word'), col('negative').alias('neg_prob'))
    .sort('neg_prob', ascending=False))


# In[12]:

import pandas as pd
pd.set_option('display.max_rows', 100)

pd.concat(
    [ positive_predictive_words.limit(100).toPandas(),
      negative_predictive_words.limit(100).toPandas() ],
    axis=1)

