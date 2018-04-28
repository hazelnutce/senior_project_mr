import numpy as np
from pythainlp.tokenize import word_tokenize
from collections import Counter, OrderedDict
from sklearn.feature_extraction import DictVectorizer
from model.aspect import aspect_predict
from model.sentiment import sentiment_predict
import numpy as np
import re


def function_caller(text):
    return [aspect_predict(text), sentiment_predict(text)]




