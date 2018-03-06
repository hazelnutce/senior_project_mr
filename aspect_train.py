from pythainlp.tokenize import word_tokenize
from pythainlp.rank import rank
from pythainlp.corpus import stopwords
from pythainlp.tag import pos_tag
from pythainlp.corpus import wordnet
from nltk.classify.scikitlearn import SklearnClassifier
import nltk
from sklearn.naive_bayes import MultinomialNB,  BernoulliNB

import io
import random
import pickle
import os
import json
import operator

from associated_func import findAssociationWord
######################################################
########select adjective list from pantip#############
######################################################

#keep separated word in this set of array
sentences = [] #for each line
documents = [] #for each topic

word_all = []
word_all_eng = []
word_all_thai_unfiltered = []
word_all_thai_filtered = []
word_all_mix = []

adjective_word = []
adjective_word_by_pos_tagging = []


#keep word that must delete in this set of array
word_preposition = []
double_char = []
positive_adjective = []
negative_adjective = []
stopwords = stopwords.words("thai")

dirName = "document/pantip_data/"

for fileName in os.listdir(dirName):
    data = json.loads(open(dirName+fileName, encoding="utf8").read())
    documents.append(data["text"])

for document in documents:
    for line in document.split("\n"):
        if(line != ""):
            sentences.append(line)

def convertFileToList(pathName, appendingList):
    with io.open(pathName, "r", encoding="utf8") as f:
        text = f.read()

    for word in text.split("\n"):
        appendingList.append(word)

convertFileToList("document/general_data/preposition.txt", word_preposition)
convertFileToList("document/general_data/double_char.txt", double_char)
convertFileToList("document/general_data/negative_adjective.txt", negative_adjective)
convertFileToList("document/general_data/positive_adjective.txt", positive_adjective)

# #print(document)
# #mm can separate all in any sentence any form
# #dict can"t separate english and whitespace because
# #it depend on thaidict in corpus
#for text in sentences:
#     word_in_text = word_tokenize(text, engine="mm")
#     for word in word_in_text:
#          word_all.append(word)
#          count_char_eng = 0
#          count_char_thai = 0
#          for character in word:
#              if(character < "z"):
#                  count_char_eng += 1
#              else:
#                  count_char_thai += 1
#          if count_char_eng == 0 and count_char_thai > 0:
#              word_all_thai.append(word)
#          elif(count_char_eng > 0 and count_char_thai == 0):
#              word_all_eng.append(word)
#          else:
#              word_all_mix.append(word)
#
# print("length of list word_all is ", len(word_all))
# print("length of list word_all_thai is ", len(word_all_thai))
# print("length of list word_all_eng is ", len(word_all_eng))
# print("length of list word_all_mix is ", len(word_all_mix))
#
# #print(pos_tag(word_all_thai, engine="old"))
# for word in word_all_thai:
#     if(word in stopwords):
#         word_all_thai.remove(word)
#
# for word in word_all_thai:
#     if(word in stopwords):
#         word_all_thai.remove(word)
#
# for word in word_all_thai:
#     if(word in stopwords):
#         word_all_thai.remove(word)
# # "ตัวหนัง": 12,  "ภาพยนตร์": 11,  "ใคร": 11,  "บท": 11,  "บอก": 11,  "ตัวละคร": 11
# for word in word_all_thai:
#     if(word in word_preposition):
#         word_all_thai.remove(word)
#
# for word in word_all_thai:
#     if(word in word_preposition):
#         word_all_thai.remove(word)
#
# for word in word_all_thai:
#     if(word in word_preposition):
#         word_all_thai.remove(word)
#
# for word in word_all_thai:
#     if (len(word) == 1):
#         word_all_thai.remove(word)
#
# for word in word_all_thai:
#     if (len(word) == 1):
#         word_all_thai.remove(word)
#
# for word in word_all_thai:
#     if (len(word) == 1):
#         word_all_thai.remove(word)
#
# for word in word_all_thai:
#     if (word in double_char):
#         word_all_thai.remove(word)
#
# for word in word_all_thai:
#     if (word in double_char):
#         word_all_thai.remove(word)
#
# for word in word_all_thai:
#     if (word in double_char):
#         word_all_thai.remove(word)
#
# print(rank(word_all_thai))

aspect_generic_word = ["หนัง", "บท", "เรื่องราว", "ภาพยนตร์", "เนื้อเรื่อง", "เล่า", "เนื้อหา", "ตัวหนัง", "บรรยากาศ", "พล็อต", "องค์ประกอบ", "องค์ประกอบโดยรวม", "ดำเนินเรื่อง", "เดินเรื่อง", "บทหนัง", "เส้นเรื่อง", "การเล่าเรื่อง", "ฉบับนี้"]
aspect_sound_word = ["เพลง", "แนวเพลง", "เสียง", "จังหวะ", "ดนตรี", "เพลงบรรยาย", "Musical", "มิวสิคัล", "มิวสิค", "เพลงประกอบภาพยนตร์"]
aspect_actor_word = ["ตัวละคร", "นักแสดง", "พระเอก", "การแสดง", "ผู้กำกับ", "นางเอก", "แสดง", "ผู้ชาย", "รับบท", "บทบาท", "ดารา", "หญิง", "คาแรกเตอร์"]
aspect_graphic_word = ["ฉาก", "ภาพ", "มุมกล้อง", "ซีน", "กล้อง", "ถ่ายทำ", "ระเบิด", "ลำดับภาพ", "เทคนิคภาพ", "เทคนิคภาพ", "ความสวยงาม", "เอฟเฟค"]

save_documents = open("pickled_aspect/aspect_generic.pickle", "wb")
pickle.dump(aspect_generic_word,  save_documents)
save_documents.close()

save_documents = open("pickled_aspect/aspect_sound.pickle", "wb")
pickle.dump(aspect_sound_word,  save_documents)
save_documents.close()

save_documents = open("pickled_aspect/aspect_actor.pickle", "wb")
pickle.dump(aspect_actor_word,  save_documents)
save_documents.close()

save_documents = open("pickled_aspect/aspect_graphic.pickle", "wb")
pickle.dump(aspect_graphic_word,  save_documents)
save_documents.close()



