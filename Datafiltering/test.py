import pymongo
import pandas as pd
from datatextCNN import init_data,textCNNFilter
import os

stopwords,model,word_index = init_data()
conn = pymongo.MongoClient('mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "152.136.59.62", "27017", "admin"))
db = conn.SocialMedia
data_test = db.posts.find().limit(100)
data_test = list(data_test)
data_train = []
for i in data_test:
    data=textCNNFilter(i,model, word_index, stopwords)
    print(data['label'])
pd.DataFrame({"co": data_train})

