import nltk
import random
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify.scikitlearn import SklearnClassifier
import numpy as np

def tenFoldValidation(featuresets,featureSize):
    accNaiveBayes = []
    accMNB = []
    accBernoulliNB = []
    accLogisticRegression = []
    accLinearSVC = []
    accSGDC = []
    accNuSVC = []
    for i in range(0,10):
        testing_set = featuresets[int(featureSize/10*i):int(featureSize/10*(i+1))]
        training_set = featuresets[0:int(featureSize/10*i)]
        training_set.extend(featuresets[int(featureSize/10*(i+1)):featureSize])
        classifier = nltk.NaiveBayesClassifier.train(training_set)
        print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set)) * 100)
        accNaiveBayes.append((nltk.classify.accuracy(classifier, testing_set)) * 100)

        MNB_classifier = SklearnClassifier(MultinomialNB())
        MNB_classifier.train(training_set)
        print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set)) * 100)
        accMNB.append((nltk.classify.accuracy(MNB_classifier, testing_set)) * 100)

        BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
        BernoulliNB_classifier.train(training_set)
        print("BernoulliNB_classifier accuracy percent:",
              (nltk.classify.accuracy(BernoulliNB_classifier, testing_set)) * 100)
        accBernoulliNB.append((nltk.classify.accuracy(BernoulliNB_classifier, testing_set)) * 100)

        LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
        LogisticRegression_classifier.train(training_set)
        print("LogisticRegression_classifier accuracy percent:",
              (nltk.classify.accuracy(LogisticRegression_classifier, testing_set)) * 100)
        accLogisticRegression.append((nltk.classify.accuracy(LogisticRegression_classifier, testing_set)) * 100)

        LinearSVC_classifier = SklearnClassifier(LinearSVC())
        LinearSVC_classifier.train(training_set)
        print("LinearSVC_classifier accuracy percent:",
              (nltk.classify.accuracy(LinearSVC_classifier, testing_set)) * 100)
        accLinearSVC.append((nltk.classify.accuracy(LinearSVC_classifier, testing_set)) * 100)

        SGDC_classifier = SklearnClassifier(SGDClassifier(max_iter=1000))
        SGDC_classifier.train(training_set)
        print("SGDClassifier accuracy percent:", nltk.classify.accuracy(SGDC_classifier, testing_set) * 100)
        accSGDC.append(nltk.classify.accuracy(SGDC_classifier, testing_set) * 100)

        NuSVC_classifier = SklearnClassifier(NuSVC())
        NuSVC_classifier.train(training_set)
        print("NuSVC_classifier accuracy percent:", (nltk.classify.accuracy(NuSVC_classifier, testing_set)) * 100)
        accNuSVC.append((nltk.classify.accuracy(NuSVC_classifier, testing_set)) * 100)

        print("-----------------------------------------")
    print("average accuracy")
    print("Naive Bayes ",np.mean(accNaiveBayes))
    print("MNB ",np.mean(accMNB))
    print("BernoulliNB ",np.mean(accBernoulliNB))
    print("LogisticRegression ",np.mean(accLogisticRegression))
    print("LinearSVC ",np.mean(accLinearSVC))
    print("SGDC ",np.mean(accSGDC))
    print("NuSVC ",np.mean(accNuSVC))