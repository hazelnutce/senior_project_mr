
from pythainlp.tokenize import word_tokenize
from pythainlp.rank import rank
from pythainlp.tag import pos_tag
from pythainlp.corpus import wordnet
import io

#keep separated word in this set of array
document = []
word_all = []
word_all_eng = []
word_all_thai = []
word_all_mix = []

#keep word that must delete in this set of array
word_preposition = []
double_char = []

with io.open('data.txt','r',encoding='utf8') as f:
    text = f.read()
    text = text.replace('\xa0',' ')

for line in text.split('\n'):
    for comment in line.split(','):
        comment.replace('',' ')
        document.append(comment)
        break

with io.open('preposition.txt','r',encoding='utf8') as f:
    text = f.read()

for word_prep in text.split('\n'):
    word_preposition.append(word_prep)

with io.open('double_char.txt','r',encoding='utf8') as f:
    text = f.read()

for dchar in text.split('\n'):
    double_char.append(dchar)

#print(document)
#mm can separate all in any sentence any form
#dict can't separate english and whitespace because
#it depend on thaidict in corpus
for text in document:
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