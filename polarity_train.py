
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
import os
import json
import operator


#keep separated word in this set of array
sentences = []
documents = []
word_all = []
word_all_eng = []
word_all_thai_unfiltered = []
word_all_thai_filtered = []
word_all_mix = []
positive_adjective = []
negative_adjective = []
adjective_word = []
adjective_word_by_pos_tagging = []

#global variable
dirName = 'document/pantip_data/'

#keep word that must delete in this set of array
word_preposition = []
double_char = []
stopwords = stopwords.words('thai')

for fileName in os.listdir(dirName):
    data = json.loads(open(dirName+fileName,encoding="utf8").read())
    documents.append(data["text"])

for document in documents:
    for line in document.split('\n'):
        if(line != ""):
            sentences.append(line)

# #save document in pickle form
# save_documents = open("pickled_polarity/documents.pickle","wb")
# pickle.dump(documents, save_documents)
# save_documents.close()

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

with io.open('document/negative_adjective.txt','r',encoding='utf8') as f:
    text = f.read()

for word_neg_adj in text.split('\n'):
    negative_adjective.append(word_neg_adj)

with io.open('document/positive_adjective.txt','r',encoding='utf8') as f:
    text = f.read()

for word_pos_adj in text.split('\n'):
    positive_adjective.append(word_pos_adj)

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
             word_all_thai_unfiltered.append(word)
         elif(count_char_eng > 0 and count_char_thai == 0):
             word_all_eng.append(word)
         else:
             word_all_mix.append(word)

# print("length of list word_all is ",len(word_all))
# print("length of list word_all_thai is ", len(word_all_thai_unfiltered))
# print("length of list word_all_eng is ",len(word_all_eng))
# print("length of list word_all_mix is ",len(word_all_mix))

#print(pos_tag(word_all_thai,engine='old'))
for word in word_all_thai_unfiltered:
    if(word not in stopwords and (word not in word_preposition) and (word not in double_char) and (len(word) > 1)):
        word_all_thai_filtered.append(word)

for word in word_all_thai_unfiltered:
    if(word in negative_adjective or word in positive_adjective):
        adjective_word.append(word)

tag_counter = []
print(rank(word_all_thai_unfiltered))
print(rank(word_all_thai_filtered))
item = rank(word_all_thai_filtered)

with open('document/data.json','w',encoding="utf-8") as fp:
    json.dump(item,fp,indent=4,ensure_ascii=False,sort_keys=True)
    # json.dump(rank(word_all_thai_filtered),fp,indent=4,ensure_ascii=False,sort_keys=True)

# pos tagger part
# for (word,tag) in pos_tag(word_all_thai_filtered,engine="old"):
#     tag_counter.append(tag)
#     if(tag is not None and tag[0] == 'V'):
#         adjective_word_by_pos_tagging.append(word)
#
# tag_counter = set(tag_counter)
# print(rank(adjective_word))
# print(rank(adjective_word_by_pos_tagging))
# print(tag_counter)

# word_counter = {}
# for word in word_all_thai_unfiltered:
#     if word in word_counter:
#         word_counter[word] += 1
#     else:
#         word_counter[word] = 1
#
# popular_words = sorted(word_counter, key = word_counter.get, reverse = True)
# word_features = popular_words[:3]
#
# def find_features(document):
#     words = word_tokenize(document,engine="mm")
#     features = {}
#     #return features if document is have only thai word
#     for word in words:
#         count_char_eng = 0
#         count_char_thai = 0
#         for character in word:
#             if (character < 'z'):
#                 count_char_eng += 1
#             else:
#                 count_char_thai += 1
#         if count_char_eng == 0 and count_char_thai > 0:
#             for w in word_features:
#                 features[w] = (w in words)
#
#     return features
#
# featuresets = [(find_features(rev), category) for (rev, category) in documents]
# random.shuffle(featuresets)
# print(len(featuresets))
#
# training_set = featuresets[:20]
# testing_set = featuresets[20:]

# classifier = nltk.NaiveBayesClassifier.train(training_set)
# print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set))*100)
# classifier.show_most_informative_features(15)
#
# ###############
# save_classifier = open("pickled_polarity/naivebayes.pickle","wb")
# pickle.dump(classifier, save_classifier)
# save_classifier.close()





