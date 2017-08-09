# from sklearn.feature_extraction.text import CountVectorizer
# vectorizer = CountVectorizer(stop_words=['this','the','is'])
#
# train_set = ("The sky is blue.", "The sun is bright.")
# test_set = ("The sun in the sky is bright.","We can see the shining sun, the bright sun.")
#
# vectorizer.fit_transform(train_set)
# smatrix = vectorizer.transform(test_set)
# print(vectorizer.vocabulary_)
# print(smatrix.todense())

import re
pat_list = """\
เc็c
เcctาะ
เccีtยะ
เccีtย(?=[เ-ไก-ฮ]|$)
เccอะ
เcc็c
เcิc์c
เcิtc
เcีtยะ?
เcืtอะ?
เc[ิีุู]tย(?=[เ-ไก-ฮ]|$)
เctา?ะ?
cัtวะ
c[ัื]tc[ุิะ]?
c[ิุู]์
c[ะ-ู]t
c็
ct[ะาำ]?
แc็c
แcc์
แctะ
แcc็c
แccc์
โctะ
[เ-ไ]ct
ๆ
ฯลฯ
ฯ
""".replace('c','[ก-ฮ]').replace('t', '[่-๋]?').split()

def tcc(w):
    p = 0 # position
    while p<len(w):
        for pat in pat_list:
            m = re.match(pat, w[p:])
            if m:
                n = m.span()[1]
                break
            else: # กรณีหาไม่เจอ
                n = 1
        yield w[p:p+n]
        p += n
def tcc1(w):
    p = 0
    pat = re.compile("|".join(pat_list))
    while p<len(w):
        m = pat.match(w[p:])
        if m:
            n = m.span()[1]
        else:
            n = 1
        yield w[p:p+n]
        p += n
def tcc(w, sep='/'):
    return sep.join(tcc1(w))
if __name__ == '__main__':
    print(tcc('แมวกิน'))
    print(tcc('ประชาชน'))
    print(tcc('ขุด')+'/'+tcc('หลุม'))
    print(tcc('ยินดี'))