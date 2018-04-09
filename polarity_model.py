import random
import pickle
from nltk.classify.scikitlearn import SklearnClassifier
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize

#function from pythainlp
from pythainlp.tokenize import word_tokenize

wordFeature_f = open("pickled_polarity/WordFeature.pickle", "rb")
featureWord = pickle.load(wordFeature_f)
wordFeature_f.close()

class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf

def find_features(document):
    words = word_tokenize(document,engine="newmm")
    words = [x for x in words if x != ""]
    print(words)
    features = {}
    willRemoveList = []
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

    for w in featureWord:
        if(w in words):
            print(w)
            count += 1
        features[w] = (w in words)
    # print(count)
    # print(words)
    return features

featuresets_f = open("pickled_polarity/FeatureSet.pickle", "rb")
featuresets = pickle.load(featuresets_f)
featuresets_f.close()

random.shuffle(featuresets)

open_file = open("pickled_polarity/NaiveBayes_classifier.pickle", "rb")
NaiveBayes_classifier = pickle.load(open_file)
open_file.close()

open_file = open("pickled_polarity/MNB_classifier.pickle", "rb")
MNB_classifier = pickle.load(open_file)
open_file.close()

open_file = open("pickled_polarity/BernoulliNB_classifier.pickle", "rb")
BernoulliNB_classifier = pickle.load(open_file)
open_file.close()

open_file = open("pickled_polarity/LogisticRegression_classifier.pickle", "rb")
LogisticRegression_classifier = pickle.load(open_file)
open_file.close()

open_file = open("pickled_polarity/LinearSVC_classifier.pickle", "rb")
LinearSVC_classifier = pickle.load(open_file)
open_file.close()

open_file = open("pickled_polarity/SGDC_classifier.pickle", "rb")
SGDC_classifier = pickle.load(open_file)
open_file.close()

open_file = open("pickled_polarity/NuSVC_classifier.pickle", "rb")
NuSVC_classifier = pickle.load(open_file)
open_file.close()

voted_classifier = VoteClassifier(
                                  NaiveBayes_classifier,
                                  LinearSVC_classifier,
                                  MNB_classifier,
                                  BernoulliNB_classifier,
                                  LogisticRegression_classifier,
                                  NuSVC_classifier,
                                  SGDC_classifier)

def sentimentSeparator(text):
    feats = find_features(text)
    return voted_classifier.classify(feats),voted_classifier.confidence(feats)

print(sentimentSeparator('CG กากมากเลย'))
