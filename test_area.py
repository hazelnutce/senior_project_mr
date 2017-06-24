from pythainlp.tokenize import word_tokenize
import io

word_thai_list = []

with io.open('thai-wordlist.txt','r',encoding='utf8') as f:
    text = f.read()

for word in text.split('\n'):
    word_thai_list.append(word)
print(word_thai_list)