from pythainlp.tokenize import word_tokenize
import json
import os
import numpy as np

#function from nltk library
import nltk
import random
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize

#function from pythainlp
from pythainlp.tokenize import word_tokenize

dirName = 'C:\\Users\\nutaw\\PycharmProjects\\senior_project\\document\\'
documentDirNamePos = dirName+'pantip_data_tmp\\pos\\'
documentDirNameNeg = dirName+'pantip_data_tmp\\neg\\'

documents = []
filenames = []
featureWord = []
general_data = "general_data\\data.json"
adjective_data = "adjective_list.json"

data = json.loads(open(dirName+adjective_data,encoding="utf8").read())
for key in data:
    featureWord.append(key)

save_featureword = open("pickled_polarity/WordFeature.pickle","wb")
pickle.dump(featureWord,save_featureword)
save_featureword.close()

for fileName in os.listdir(documentDirNamePos):
    data = json.loads(open(documentDirNamePos + fileName, encoding="utf8").read())
    documents.append((data["text"],"pos",fileName))
    filenames.append(fileName)

for fileName in os.listdir(documentDirNameNeg):
    data = json.loads(open(documentDirNameNeg + fileName, encoding="utf8").read())
    documents.append((data["text"],"neg",fileName))
    filenames.append(fileName)

featureSize = len(documents)
print(featureSize)

def find_features(document,fileName):
    #we add fileName because detected no-keyword file
    words = word_tokenize(document,engine="newmm")
    words = [x for x in words if x != ""]
    willRemoveList = []
    #5-grams
    for i in range(0, len(words) - 4):
        if (words[i] + words[i + 1] + words[i + 2] + words[i + 3] + words[i + 4] in featureWord):
            words.append(words[i] + words[i + 1] + words[i + 2] + words[i + 3] + words[i + 4])
            willRemoveList.extend([words[i], words[i + 1], words[i + 2], words[i + 3], words[i + 4]])
    # 4-grams
    for i in range(0, len(words) - 3):
        if (words[i] + words[i + 1] + words[i + 2] + words[i + 3] in featureWord):
            words.append(words[i] + words[i + 1] + words[i + 2] + words[i + 3])
            willRemoveList.extend([words[i], words[i + 1], words[i + 2], words[i + 3]])
    # tri-grams
    for i in range(0, len(words) - 2):
        if (words[i] + words[i + 1] + words[i + 2] in featureWord):
            words.append(words[i] + words[i + 1] + words[i + 2])
            willRemoveList.extend([words[i], words[i + 1], words[i + 2]])
    # bi-grams
    for i in range(0, len(words) - 1):
        if (words[i] + words[i + 1] in featureWord):
            words.append(words[i] + words[i + 1])
            willRemoveList.extend([words[i], words[i + 1]])

    words = [x for x in words if x not in willRemoveList]
    count = 0
    features = {}
    #return features if document is have only thai word
    for w in featureWord:
        if(w in words):
            count+=1
        features[w] = (w in words)
    if(count == 0):
        print(fileName)
    # print(count)
    return features

featuresets = [(find_features(comment,fileName), category) for (comment, category,fileName) in documents]
random.shuffle(featuresets)

save_featuresets = open("pickled_polarity/FeatureSet.pickle","wb")
pickle.dump(featuresets,save_featuresets)
save_featuresets.close()

trainLength = int(featureSize * 0.8)
training_set = featuresets[:trainLength]
testing_set = featuresets[trainLength:]

classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set))*100)

save_classifier = open("pickled_polarity/NaiveBayes_classifier.pickle","wb")
pickle.dump(classifier, save_classifier)
save_classifier.close()

MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set))*100)

save_classifier = open("pickled_polarity/MNB_classifier.pickle","wb")
pickle.dump(MNB_classifier, save_classifier)
save_classifier.close()

BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(training_set)
print("BernoulliNB_classifier accuracy percent:", (nltk.classify.accuracy(BernoulliNB_classifier, testing_set))*100)

save_classifier = open("pickled_polarity/BernoulliNB_classifier.pickle","wb")
pickle.dump(BernoulliNB_classifier, save_classifier)
save_classifier.close()

LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
print("LogisticRegression_classifier accuracy percent:", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)

save_classifier = open("pickled_polarity/LogisticRegression_classifier.pickle","wb")
pickle.dump(LogisticRegression_classifier, save_classifier)
save_classifier.close()


LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)

save_classifier = open("pickled_polarity/LinearSVC_classifier.pickle","wb")
pickle.dump(LinearSVC_classifier, save_classifier)
save_classifier.close()

SGDC_classifier = SklearnClassifier(SGDClassifier(max_iter=1000))
SGDC_classifier.train(training_set)
print("SGDClassifier accuracy percent:",nltk.classify.accuracy(SGDC_classifier, testing_set)*100)

save_classifier = open("pickled_polarity/SGDC_classifier.pickle","wb")
pickle.dump(SGDC_classifier, save_classifier)
save_classifier.close()

NuSVC_classifier = SklearnClassifier(NuSVC())
NuSVC_classifier.train(training_set)
print("NuSVC_classifier accuracy percent:", (nltk.classify.accuracy(NuSVC_classifier, testing_set))*100)

save_classifier = open("pickled_polarity/NuSVC_classifier.pickle","wb")
pickle.dump(LinearSVC_classifier, save_classifier)
save_classifier.close()
