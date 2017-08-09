
from pythainlp.tokenize import word_tokenize
from pythainlp.rank import rank
from pythainlp.corpus import stopwords
from pythainlp.tag import pos_tag
from pythainlp.corpus import wordnet
from nltk.classify.scikitlearn import SklearnClassifier
import nltk
from sklearn.naive_bayes import MultinomialNB, BernoulliNB

import io
import random
import pickle

#keep separated word in this set of array
sentences = []
documents = []
word_all = []
word_all_eng = []
word_all_thai = []
word_all_mix = []

#keep word that must delete in this set of array
word_preposition = []
double_char = []
stopwords = stopwords.words('thai')

#convert audience comment from data file to list (positive comment)
with io.open('document/data_pos.txt','r',encoding='utf8') as f:
    text = f.read()
    text = text.replace('\xa0',' ')

for line in text.split('\n'):
    sentence = line.split(',')[0].replace(' ','')
    documents.append((sentence,"pos"))
    sentences.append(sentence)

#convert audience comment from data file to list (negative comment)
with io.open('document/data_neg.txt','r',encoding='utf8') as f:
    text = f.read()
    text = text.replace('\xa0',' ')

for line in text.split('\n'):
    sentence = line.split(',')[0].replace(' ','')
    documents.append((sentence,"neg"))
    sentences.append(sentence)

#save document in pickle form
save_documents = open("pickled_algos/documents.pickle","wb")
pickle.dump(documents, save_documents)
save_documents.close()

#convert preposition word from data file to list
with io.open('document/preposition.txt','r',encoding='utf8') as f:
    text = f.read()

for word_prep in text.split('\n'):
    word_preposition.append(word_prep)

#convert double char word from data file to list
with io.open('document/double_char.txt','r',encoding='utf8') as f:
    text = f.read()

for dchar in text.split('\n'):
    double_char.append(dchar)

#print(document)
#mm can separate all in any sentence any form
#dict can't separate english and whitespace because
#it depend on thaidict in corpus
for text in sentences:
    word_in_text = word_tokenize(text,engine="mm")
    for word in word_in_text:
         word_all.append(word)
         count_char_eng = 0
         count_char_thai = 0
         for character in word:
             if(character < 'z'):
                 count_char_eng += 1
             else:
                 count_char_thai += 1
         if count_char_eng == 0 and count_char_thai > 0:
             word_all_thai.append(word)
         elif(count_char_eng > 0 and count_char_thai == 0):
             word_all_eng.append(word)
         else:
             word_all_mix.append(word)

print("length of list word_all is ",len(word_all))
print("length of list word_all_thai is ",len(word_all_thai))
print("length of list word_all_eng is ",len(word_all_eng))
print("length of list word_all_mix is ",len(word_all_mix))

#print(pos_tag(word_all_thai,engine='old'))
for word in word_all_thai:
    if(word in stopwords):
        word_all_thai.remove(word)

for word in word_all_thai:
    if(word in stopwords):
        word_all_thai.remove(word)

for word in word_all_thai:
    if(word in stopwords):
        word_all_thai.remove(word)
# 'ตัวหนัง': 12, 'ภาพยนตร์': 11, 'ใคร': 11, 'บท': 11, 'บอก': 11, 'ตัวละคร': 11
for word in word_all_thai:
    if(word in word_preposition):
        word_all_thai.remove(word)

for word in word_all_thai:
    if(word in word_preposition):
        word_all_thai.remove(word)

for word in word_all_thai:
    if(word in word_preposition):
        word_all_thai.remove(word)

for word in word_all_thai:
    if (len(word) == 1):
        word_all_thai.remove(word)

for word in word_all_thai:
    if (len(word) == 1):
        word_all_thai.remove(word)

for word in word_all_thai:
    if (len(word) == 1):
        word_all_thai.remove(word)

for word in word_all_thai:
    if (word in double_char):
        word_all_thai.remove(word)

for word in word_all_thai:
    if (word in double_char):
        word_all_thai.remove(word)

for word in word_all_thai:
    if (word in double_char):
        word_all_thai.remove(word)

print(rank(word_all_thai))

word_counter = {}
for word in word_all_thai:
    if word in word_counter:
        word_counter[word] += 1
    else:
        word_counter[word] = 1

popular_words = sorted(word_counter, key = word_counter.get, reverse = True)
word_features = popular_words[:3]

def find_features(document):
    words = word_tokenize(document,engine="mm")
    features = {}
    #return features if document is have only thai word
    for word in words:
        count_char_eng = 0
        count_char_thai = 0
        for character in word:
            if (character < 'z'):
                count_char_eng += 1
            else:
                count_char_thai += 1
        if count_char_eng == 0 and count_char_thai > 0:
            for w in word_features:
                features[w] = (w in words)

    return features

featuresets = [(find_features(rev), category) for (rev, category) in documents]
random.shuffle(featuresets)
print(len(featuresets))

training_set = featuresets[:20]
testing_set = featuresets[20:]

# classifier = nltk.NaiveBayesClassifier.train(training_set)
# print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set))*100)
# classifier.show_most_informative_features(15)
#
# ###############
# save_classifier = open("pickled_algos/naivebayes.pickle","wb")
# pickle.dump(classifier, save_classifier)
# save_classifier.close()





