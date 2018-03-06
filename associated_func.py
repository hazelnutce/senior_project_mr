import csv
import io
import re
from pythainlp.corpus import stopwords
from pythainlp.tokenize import word_tokenize
import pandas as pd
from mlxtend.preprocessing import OnehotTransactions
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import numpy as np

stopword = stopwords.words('thai')
with io.open('document/general_data/preposition.txt', 'r', encoding="utf8") as f:
    text = f.read()
    prep = re.split('[\n\r]+', text)
    stopword.extend(prep)
stopword = list(set(stopword))
dict_th = list
with io.open('document/general_data/thai-wordlist.txt','r',encoding='utf8') as f:
     text = f.read()
     dict_th = re.split('[\n\r]+', text)

def findAssociationWord(sentenceList):
    transactionID = list()
    for sentence in sentenceList:
        word_list = word_tokenize(sentence, engine='mm')
        for word in reversed(word_list):
            if word in stopword or re.match('[\W]+',word):
                word_list.remove(word)
        transactionID.append(word_list)
    oht = OnehotTransactions()
    oht_ary = oht.fit(transactionID).transform(transactionID)
    df = pd.DataFrame(oht_ary, columns=oht.columns_)
    frequent_itemsets = apriori(df, min_support=0.01, use_colnames=True)
    result = association_rules(frequent_itemsets, metric="lift", min_threshold=0.5)
    print(result)

# exampleList = list(['หนังสนุกดีนะ วันหน้าเราจะมาดูใหม่','หนังเรื่องนี้เป็นหนังรักโรแมนติกที่ไม่มีวันลืม','หนังเรื่องแบบนี้ สนุกดีนะ'])
# findAssociationWord(exampleList)
