
# coding: utf-8

# # User trustedness

# ## Loading data

# In[9]:

# all_reviews = (spark
#     .read
#     .json('../../data/raw_data/reviews_Musical_Instruments_5.json.gz'))


# ## Extracting ranking components

# In[10]:

reviews = all_reviews
reviews_per_reviewer = reviews.groupBy('reviewerID').count()


# In[31]:

from pyspark.sql.functions import col, udf, avg
from pyspark.sql.types import DoubleType

helpfulness_ratio = udf(
    lambda (useful, out_of): useful / float(out_of + 1), 
    returnType=DoubleType())

helpfulness = (reviews
  .select('reviewerID', helpfulness_ratio(col('helpful')).alias('helpfulness'))
  .groupBy('reviewerID')
  .agg(avg(col('helpfulness')).alias('helpfulness')))


# ## Computing rankings & visualizing the good and bad reviews from the most trusted users

# In[32]:

reviewers_trustedness = (helpfulness
    .join(reviews_per_reviewer, 'reviewerID')
    .select('reviewerID', (col('helpfulness') * col('count')).alias('trustedness')))


# In[ ]:

reviewers_trustedness.limit(10).toPandas()

