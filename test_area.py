from nltk.corpus import wordnet as wn

test_word = ['actor','actress','charcater','movie','good','terrible']
result_word = []

for word in test_word:
    set_synonym_word = wn.synsets(word)
    if len(set_synonym_word) > 0:
        for synonym_word in set_synonym_word:
            result_word.extend(synonym_word.lemma_names())

result_word = set(result_word)
print(result_word)

def find_max_similarity(word1,word2):
    max_similarilty = 0
    w1 = wn.synsets(word1, lang="tha")
    w2 = wn.synsets(word2, lang="tha")
    if len(w1) > 0 and len(w2) > 0:
        for word in w1:
            for word2 in w2:
                similarity_value = word.wup_similarity(word2)
                if similarity_value is not None:
                    max_similarilty = max(similarity_value, max_similarilty)
    return max_similarilty

print(find_max_similarity('รถ','เรือ'))


