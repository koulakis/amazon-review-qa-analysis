
# coding: utf-8

# In[6]:

# reviews_filepath = '../../data/raw_data/reviews_Musical_Instruments_5.json.gz'
# metadata_filepath = '../../data/metadata/meta_Musical_Instruments.json.gz'


# In[7]:

all_reviews = (spark
    .read
    .json(reviews_filepath))

all_metadata = (spark
    .read
    .json(metadata_filepath))

