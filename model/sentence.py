from pythainlp.tokenize import word_tokenize
from pythainlp.corpus import thaipos
from pythainlp import pos_tag
import tltk
import re
import pickle
import os
cwd = os.getcwd()

pos_tagger = \
    {
        'NPRP', 'NCNM', 'NONM', 'NLBL', 'NCMN',
        'NTTL', 'PPRS', 'PDMN', 'PNTR', 'PREL',
        'VACT', 'VSTA', 'VATT', 'XVBM', 'XVAM',  # 'XVBM', 'XVAM'
        'XVMM', 'XVBB', 'XVAE', 'DDAN', 'DDAC',
        'DDBC', 'DDAQ', 'DIAC', 'DIBQ', 'DIAQ',
        'DCNM', 'DONM', 'ADVN', 'ADVI', 'ADVP',
        'ADVS', 'CNIT', 'CLTV', 'CMTR', 'CFQC',
        'CVBL', 'JCRG', 'JCMP', 'JSBR', 'RPRE',
        'INT', 'FIXN', 'FIXV', 'EAFF', 'EITT',
        'NEG', 'PUNC',
        # not sure
        'DDBQ'
    }
if("\\model" in cwd):
    cwd = cwd.replace("\\model","")
open_file = open(cwd+'/model/pickle/aspect_keyword.pickle','rb')
aspect_kw = pickle.load(open_file)
open_file.close()

open_file = open(cwd+'/model/pickle/sentiment_keyword.pickle','rb')
sentiment_kw = pickle.load(open_file)
open_file.close()


def get_keyword_type(text):
    word_list = word_tokenize(text, engine='newmm')
    # pos_list = [item[1] for item in pos_tag(word_list,engine='artagger')]
    result = []
    # print(pos_list)
    if bool(set.intersection(set(word_list), aspect_kw)):
        result.append('aspect')
    if bool(set.intersection(set(word_list), sentimet_kw)):
        result.append('sentiment')
    # #
    # #
    # print(text)
    # print(result)
    return result


def is_sentence(text):
    result = tltk.pos_tag(text,'mm')
    pos_list = [item[1] for row in result for item in row if item[0] is not ' ']
    # print(result)
    # print(pos_list)

    return not bool(set.difference(set(['NOUN','VERB']), set(pos_list))) or \
           not bool(set.difference(set(['PRON','VERB']), set(pos_list))) or \
           not bool(set.difference(set(['PRONP', 'VERB']), set(pos_list)))



def sentence_cutter(text, drop_sentence=None):
    # remove another symbol
    # text = re.sub('[^A-Za-z0-9ก-๙\.,\/\-; \n\r]', ' ', text)

    # split by newline or space
    units = re.split('[\n ]+',text)
    all_sentence = []
    current_text = ''
    temp_str = ''
    for item in units:
    #     current_text = current_text + ' ' + item
    #     if is_sentence(current_text):
    #         all_sentence.append(current_text)
    #         current_text = ''
    # if not is_sentence(current_text):
    #     all_sentence.append(current_text)
        if is_sentence(item) and is_sentence(temp_str):
            all_sentence.append(temp_str)
            temp_str = item
        else:
            temp_str = temp_str + ' ' + item
    all_sentence.append(temp_str)

    if drop_sentence:
        s = []
        for item in all_sentence:
            type = get_keyword_type(item)
            if 'aspect' in type and 'sentiment' in type:
                s.append(item)
        return s
    else:
        return all_sentence



# input_text = 'นี่ไม่เคยดูภาคแรก แต่ตอนเปิดเรื่องบรรยายได้โอเค เล่าเรื่องได้ติดต่อกัน ดูไปไม่งงเลย เรื่องCGคือขั้นเทพ สวยชิบหายแล้วก็เนียนมาก ฉากสู้กันมันส์โคตรๆเสียวสุดๆมีแทรกมุกตลกเยอะ ฉากพีคก็เยอะ แต่โคตรเรื่องค่อยข้างเดาง่ายไม่ค่อยลุ้น ตัดไป 1 คะแนน'
# item_text = str('ไปดูเพราะพันทิพครับ แต่ผมไม่ชอบ ไม่ซึ้ง ไม่อิน ไม่โอเค ดูเนื้อเรื่องไม่สมเหตุสมผลเท่าไร',encoding='utf-8')
# sentence_list = sentence_cutter(input_text, drop_sentence=True)
#
# for item in sentence_list:
#     print(item)