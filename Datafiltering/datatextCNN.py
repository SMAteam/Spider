import pymongo
import pandas as pd
import re
from  keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import jieba,numpy,pandas
from gensim.models import Word2Vec
import os
#  textCNN进行垃圾的过滤

# 获取数据
#
# conn = pymongo.MongoClient('mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "152.136.59.62", "27017", "admin"))
# db = conn.SocialMedia
# data_test = db.test.find().limit(100)
# data_test = list(data_test)
# data_train = []
# for i in data_test:
#     print(i)
# pd.DataFrame({"co": data_train})


# 初始化的textCNN模型数据，避免重复加载模型
def init_data():
    stopwords = open(os.path.join(os.path.dirname(__file__),"./model/停用词表.txt"), "r", encoding="utf-8").read()
    # model=load_model('cnn地震.h5',custom_objects={'Functional': mycrossentropy })
    model = load_model(os.path.join(os.path.dirname(__file__),'./model/cnn地震2.h5'))
    model1 = load_model(os.path.join(os.path.dirname(__file__),'./model/cnn地震2.h5'))
    # model.load_weights('cnn地震2.h5')
    word2vec_model = Word2Vec.load(os.path.join(os.path.dirname(__file__),'./model/word2vec_model'))
    vocab_list = [word for word, Vocab in word2vec_model.wv.vocab.items()]
    word_index = {" ": 0}
    for i in range(len(vocab_list)):
        word = vocab_list[i]
        word_index[word] = i + 1
    return stopwords,model,word_index
# print(len(init_data()))


# 数据清洗模块
def clean_data(data):
    cleanr = '<u>.*?</u>|://weibo.*?<.@'
#     print(cleanr)
    data = re.sub(cleanr,'',data)
    data = re.sub(r'@>|:\w+:','',data)
    return data

# 联合规则化过滤，对textCNN进行重新的召回
def ReLabel(data):
    data = re.sub('瞳孔地震|笑到地震|心脏地震', '', data)
    keyword_list = ['震源', '震级', '地震局', '地震台网', '地震手册', '地震灾害','汶川','青海','玉树']
    # 检查##话题
    Regx = re.compile('<#>#.*#</#>')
    title = Regx.findall(data)
    if (title != [] and ('地震' in title[0] or '防震' in title[0] or '科普' in title[0])):
        return '1'
    # 检查关键字
    for keyword in keyword_list:
        if (keyword in data):
            return '1'
    # 进一步过滤
    if ('地震' in data and len(data) <= 20):
        if ('娱乐圈' in data or '饭圈' in data):
            return '0'
        return '1'
    return '0'


# textCNN模型
def textCNNFilter(data_test,model,word_index,stopwords):
    # 模型预测、联合过滤
    # 区分不同种类
    text = data_test['post_content']
    #'1'微博，'2'新闻
    if(data_test['media']=='2'):
        text = data_test['user_name'] + data_test['title'] + data_test['brief']
    text = clean_data(text)
    if text == '':
        data_test['label'] = '0'
        return data_test
    else:
        words = jieba.lcut(text)
    texts = []
    string = ''
    for word in words:
        if word in stopwords:
            continue
        else:
            string = string + word + ' '
    texts.append(string[:-1])
    trainDF = pandas.DataFrame()
    trainDF['text'] = texts
    data = []
    for sentence in trainDF['text']:
        new_txt = []
        for word in sentence:
            try:
                new_txt.append(word_index[word])
            except:
                new_txt.append(0)
        data.append(new_txt)
    x_padded = pad_sequences(data, maxlen=50)
    result = model.predict(x_padded)  # 预测样本属于每个类别的概率
    result_labels = numpy.argmax(result, axis=-1)  # 获得最大概率对应的标签
    result_label = str(result_labels[0])

    # 对标签为0的数据进行进一步的规则化提取
    if (result_label == '0'):
        result_label = ReLabel(text)
        # 对新闻进行正则化提取
        if (data_test['media'] == '2'):
            if ('地震' in data_test['user_name'] or '地震' in data_test['title']):
                result_label = '1'
    data_test['label'] = result_label
    print(result_labels[0])
    return data_test

