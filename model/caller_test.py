from model.function_caller import function_caller
from model.sentence import sentence_cutter
from model.aspect import aspect_predict
from model.sentiment import sentiment_predict


text_input = 'ไม่สนุก'
sentence_list = sentence_cutter('Furious 7 ห่วยแตก เสียดายเวลาที่สุดอีกเรื่องในชีวิตการดูหนัง')
print(sentence_list)

for item in sentence_list:
    print(function_caller(item))

# predict แยก
print()
text = 'ตัดต่อแย่'
aspect = aspect_predict(text)
sentiment = sentiment_predict(text)

print(aspect + '|' + sentiment)
