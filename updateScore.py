import time
from time import gmtime, strftime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import aspect_model
import polarity_model
import model.sentence
import model.aspect
import model.sentiment

cred = credentials.Certificate('test_area_file/credentialAuth.json')
default_app = firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://moviescorer-67315.firebaseio.com/'
})
movieData = []
def calculateNewScore(data,root):
    for movieKey, movieValue in data.items():
        scoreDict = {
            'soundScore': 5,
            'actorScore': 5,
            'graphicScore': 5,
            'genericScore': 5,
            'plotScore': 5,
            'averageScore': 5
        }
        score = [5, 5, 5, 5, 5]
        countComments = [0, 0, 0, 0, 0]
        countPosComments = [0, 0, 0, 0, 0]
        countNegComments = [0, 0, 0, 0, 0]
        try:
            # comments iteration
            # for i,j in movieValue['comments'].items():
            #     print("--",j["comment"])
            for commentKey, commentValue in movieValue['comments'].items():
                # print("--",commentValue["comment"])
                posComment = 0
                negComment = 0
                # print(commentValue['comment'])
                sentence_list = model.sentence.sentence_cutter(commentValue["comment"])
                sentenceString = ""
                aspectString = ""
                sentimentString = ""
                for sentence in sentence_list:
                    sentenceString += (sentence+"/")
                    sentimentAns,probAns,count = polarity_model.sentimentSeparator(sentence)
                    if(count == 0):
                        sentimentAns = model.sentiment.sentiment_predict(sentence)
                    aspectAns = model.aspect.aspect_predict(sentence)
                    aspectString += (aspectAns+"/")
                    sentimentString += (sentimentAns+"/")
                    print(aspectAns)
                    new_sentiment = root.child('movies/' + movieKey + '/comments/' + commentKey).update(
                        {'sentenceLength': len(sentence_list)})
                    if aspectAns == 'general':
                        countComments[0] += 1
                        if sentimentAns == 'pos' and probAns > 0.7:
                            countPosComments[0] += 1
                            posComment += 1
                        elif sentimentAns == 'neg' and probAns > 0.7:
                            countNegComments[0] += 1
                            negComment += 1
                    elif aspectAns == 'graphic':
                        countComments[1] += 1
                        if sentimentAns == 'pos' and probAns > 0.7:
                            countPosComments[1] += 1
                            posComment += 1
                        elif sentimentAns == 'neg' and probAns > 0.7:
                            countNegComments[1] += 1
                            negComment += 1
                    elif aspectAns == 'sound':
                        countComments[2] += 1
                        if sentimentAns == 'pos' and probAns > 0.7:
                            countPosComments[2] += 1
                            posComment += 1
                        elif sentimentAns == 'neg' and probAns > 0.7:
                            countNegComments[2] += 1
                            negComment += 1
                    elif aspectAns == 'actor':
                        countComments[3] += 1
                        if sentimentAns == 'pos' and probAns > 0.7:
                            countPosComments[3] += 1
                            posComment += 1
                        elif sentimentAns == 'neg' and probAns > 0.7:
                            countNegComments[3] += 1
                            negComment += 1
                    elif aspectAns == 'plot':
                        countComments[4] += 1
                        if sentimentAns == 'pos' and probAns > 0.7:
                            countPosComments[4] += 1
                            posComment += 1
                        elif sentimentAns == 'neg' and probAns > 0.7:
                            countNegComments[4] += 1
                            negComment += 1
                    # want to update pos/neg attribute to database
                if (posComment > negComment):
                    # print(commentValue["comment"], "pos", probAns, movieValue["movieName"])
                    new_sentiment = root.child('movies/' + movieKey + '/comments/' + commentKey).update({
                        'sentiment': 'pos','status': 'complete','sentenceLength': len(sentence_list),
                        'sentenceSplit': sentenceString,'aspectSplit': aspectString,'sentimentSplit' : sentimentString})
                elif(negComment > posComment):
                    # print(commentValue["comment"], "neg", probAns, movieValue["movieName"])
                    new_sentiment = root.child('movies/' + movieKey + '/comments/' + commentKey).update({
                        'sentiment': 'neg','status': 'complete','sentenceLength': len(sentence_list),
                        'sentenceSplit': sentenceString,'aspectSplit': aspectString,'sentimentSplit' : sentimentString})
                else:
                    new_sentiment = root.child('movies/' + movieKey + '/comments/' + commentKey).update(
                        {'sentiment': 'neu', 'status': 'complete','sentenceLength': len(sentence_list),
                         'sentenceSplit': sentenceString,'aspectSplit': aspectString,'sentimentSplit' : sentimentString})
            countIndex = 0
            for c, d, e, f in zip(countComments, countPosComments, countNegComments, score):
                if c > 25:
                    f = f + d * 1.0 / c * 5.0 - e * 1.0 / c * 5.0
                else:
                    f = f + d * 0.2 - e * 0.2
                score[countIndex] = round(f,1)
                countIndex += 1
            scoreDict['genericScore'] = score[0]
            scoreDict['graphicScore'] = score[1]
            scoreDict['soundScore'] = score[2]
            scoreDict['actorScore'] = score[3]
            scoreDict['plotScore'] = score[4]
            scoreDict['averageScore'] = round((score[0]+score[1]+score[2]+score[3]+score[4])/5.0,1)
            new_score = root.child('movies/' + movieKey).update(scoreDict)
            # print(countPosComment)
            # print(countNegComment)
        except KeyError:
            continue

preSum = 0
while (True):
    data = db.reference('movies').get()
    root = db.reference()
    sum = 0
    for movieKey, movieValue in data.items():
        try:
            for commentKey,commentValue in movieValue['comments'].items():
                sum = sum + 1
        except KeyError:
            continue
    if sum != preSum:
        preSum = sum
        print("Calculating ",sum,"comments",strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        calculateNewScore(data,root)
        print("Calculation complete ", strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    else:
        preSum = sum
        print("Nothing Change", strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        time.sleep(2)
    time.sleep(3)




