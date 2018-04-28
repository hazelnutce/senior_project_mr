from sklearn.feature_extraction import DictVectorizer
from pythainlp.tokenize import word_tokenize
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from collections import Counter, OrderedDict
import pickle
import numpy as np

open_file = open('pickle/sentiment_keyword.pickle','rb')
sentiment_kw = pickle.load(open_file)
open_file.close()

open_file = open('pickle/sentiment_classifier.pickle','rb')
sentiment_classifier = pickle.load(open_file)
open_file.close()

# sentiment_file_path = '../dict/sentiment/dict_sentiment v2.txt'
# with open(sentiment_file_path, encoding='utf8') as data_file:
#     data = data_file.read()
#     sentiment_kw = set(data.split('\n'))


def bag(text):
    temp = word_tokenize(text, engine='newmm')
    v = DictVectorizer()
    v.fit([OrderedDict.fromkeys(sentiment_kw)])
    max_ngram = 3
    ngram_list = []
    for n in reversed(range(2, max_ngram + 1)):
        for i in range(len(temp) - n + 1):
            ngram_list.append(temp[i:i + n])

    remove_word = []
    for item in ngram_list:
        new_word = ''.join(item)
        if new_word in sentiment_kw:
            temp.append(new_word)
            remove_word.extend(item)

    output = [w for w in temp if w not in remove_word]
    output = set.intersection(set(output), sentiment_kw)
    X = v.fit_transform(Counter(i) for i in [sentiment_kw, output])
    return X[1]

text = 'หารดูหนังที่อึดอัดมากที่สุดดูจบ'
# print(sentiment_classifier.predict(bag(text)))

def sentiment_predict(text):
    pred = sentiment_classifier.predict(bag(text))

    # covert ndarray to string
    return pred[0]
