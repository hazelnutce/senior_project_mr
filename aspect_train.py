# import io
# import random
import pickle
#
# from pythainlp.tokenize import word_tokenize
# from pythainlp.rank import rank
# from pythainlp.corpus import stopwords
#
# #keep separated word in this set of array
# sentences = []
# documents = []
# word_all = []
# word_all_eng = []
# word_all_thai = []
# word_all_mix = []
#
# #keep word that must delete in this set of array
# word_preposition = []
# double_char = []
# stopwords = stopwords.words('thai')
#
# #convert audience comment from data file to list (positive comment)
# with io.open('document/data_pos.txt','r',encoding='utf8') as f:
#     text = f.read()
#     text = text.replace('\xa0',' ')
#
# for line in text.split('\n'):
#     sentence = line.split(',')[0].replace(' ','')
#     documents.append((sentence,"pos"))
#     sentences.append(sentence)
#
# #convert audience comment from data file to list (negative comment)
# with io.open('document/data_neg.txt','r',encoding='utf8') as f:
#     text = f.read()
#     text = text.replace('\xa0',' ')
#
# for line in text.split('\n'):
#     sentence = line.split(',')[0].replace(' ','')
#     documents.append((sentence,"neg"))
#     sentences.append(sentence)
#
# #save document in pickle form
# save_documents = open("pickled_aspect/documents.pickle","wb")
# pickle.dump(documents, save_documents)
# save_documents.close()
#
# #convert preposition word from data file to list
# with io.open('document/preposition.txt','r',encoding='utf8') as f:
#     text = f.read()
#
# for word_prep in text.split('\n'):
#     word_preposition.append(word_prep)
#
# #convert double char word from data file to list
# with io.open('document/double_char.txt','r',encoding='utf8') as f:
#     text = f.read()
#
# for dchar in text.split('\n'):
#     double_char.append(dchar)
#
# #print(document)
# #mm can separate all in any sentence any form
# #dict can't separate english and whitespace because
# #it depend on thaidict in corpus
# for text in sentences:
#     word_in_text = word_tokenize(text,engine="mm")
#     for word in word_in_text:
#          word_all.append(word)
#          count_char_eng = 0
#          count_char_thai = 0
#          for character in word:
#              if(character < 'z'):
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
# print("length of list word_all is ",len(word_all))
# print("length of list word_all_thai is ",len(word_all_thai))
# print("length of list word_all_eng is ",len(word_all_eng))
# print("length of list word_all_mix is ",len(word_all_mix))
#
# #print(pos_tag(word_all_thai,engine='old'))
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
# # 'ตัวหนัง': 12, 'ภาพยนตร์': 11, 'ใคร': 11, 'บท': 11, 'บอก': 11, 'ตัวละคร': 11
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

aspect_generic_word = ['ทั่วไป']
aspect_sound_word = ['เสียง']
aspect_actor_word = ['นักแสดง']
aspect_graphic_word = ['กราฟิก','ภาพ']

save_documents = open("pickled_aspect/aspect_generic.pickle","wb")
pickle.dump(aspect_generic_word, save_documents)
save_documents.close()

save_documents = open("pickled_aspect/aspect_sound.pickle","wb")
pickle.dump(aspect_sound_word, save_documents)
save_documents.close()

save_documents = open("pickled_aspect/aspect_actor.pickle","wb")
pickle.dump(aspect_actor_word, save_documents)
save_documents.close()

save_documents = open("pickled_aspect/aspect_graphic.pickle","wb")
pickle.dump(aspect_graphic_word, save_documents)
save_documents.close()



