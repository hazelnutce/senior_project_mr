from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier
from pythainlp.tokenize import word_tokenize
from collections import Counter, OrderedDict
import pickle
import os

# save pickle
# a = ['a','b','c']
# save_var = open('a.pickle','wb')
# pickle.dump(a, save_var)
# save_var.close()
cwd = os.getcwd()
print(cwd)
if("\\model" in cwd):
    cwd = cwd.replace("\\model","")
open_file = open(cwd+'/model/pickle/aspect_keyword.pickle','rb')
aspect_kw = pickle.load(open_file)
open_file.close()
# open
open_file = open(cwd+'/model/pickle/aspect_classifier.pickle','rb')
aspect_classifier = pickle.load(open_file)
open_file.close()

# aspect_file_path = '../dict/aspect v2/dict_aspect.txt'
# with open(aspect_file_path, encoding='utf8') as data_file:
#     data = data_file.read()
#     aspect_kw = set(data.split('\n'))


# text = 'ลายเส้นโคตรเนี้ยบ'
def bag(text):
    v = DictVectorizer()
    v.fit([OrderedDict.fromkeys(aspect_kw)])
    temp = set(word_tokenize(text, engine='newmm'))
    X = v.fit_transform(Counter(i) for i in [aspect_kw, set.intersection(temp, aspect_kw)])
    return X[1]

# input = bag(text)
# print(aspect_classifier.predict(input))
# print(aspect_classifier.predict(bag('CGกาก')))
def aspect_predict(text):
    input = bag(text)
    pred = aspect_classifier.predict(input)

    # covert ndarray to string

    return pred[0]