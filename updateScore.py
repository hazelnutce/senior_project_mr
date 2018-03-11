import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import aspect_model
import polarity_model

cred = credentials.Certificate('test_area_file/credentialAuth.json')
default_app = firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://moviescorer-67315.firebaseio.com/'
})

data = db.reference('movies').get()
root = db.reference()
movieData = []

#update score
for movieKey,movieValue in data.items():
    scoreDict = {
        'soundScore' : 5,
        'actorScore' : 5,
        'graphicScore' : 5,
        'genericScore' : 5
    }
    score = [5,5,5,5]
    countComment = [0,0,0,0]
    countPosComment = [0,0,0,0]
    countNegComment = [0,0,0,0]
    try:
        for commentKey,commentValue in movieValue['comments'].items():
            commentsLength = len(movieValue['comments'].items())
            print(commentValue['comment'])
            sentimentAns,probAns = polarity_model.sentimentSeparator(commentValue['comment'])
            aspectsAns = aspect_model.aspectSeparator(commentValue['comment'])
            for aspect in aspectsAns:
                if aspect == 'generic':
                    countComment[0] += 1
                    if sentimentAns == 'pos' and probAns > 0.7:
                        countPosComment[0] += 1
                    elif sentimentAns == 'neg' and probAns > 0.7:
                        countNegComment[0] += 1
                elif aspect == 'graphic':
                    countComment[1] += 1
                    if sentimentAns == 'pos' and probAns > 0.7:
                        countPosComment[1] += 1
                    elif sentimentAns == 'neg' and probAns > 0.7:
                        countNegComment[1] += 1
                elif aspect == 'sound':
                    countComment[2] += 1
                    if sentimentAns == 'pos' and probAns > 0.7:
                        countPosComment[2] += 1
                    elif sentimentAns == 'neg' and probAns > 0.7:
                        countNegComment[2] += 1
                elif aspect == 'actor':
                    countComment[3] += 1
                    if sentimentAns == 'pos' and probAns > 0.7:
                        countPosComment[3] += 1
                    elif sentimentAns == 'neg' and probAns > 0.7:
                        countNegComment[3] += 1
        countIndex = 0
        for c,d,e,f in zip(countComment,countPosComment,countNegComment,score):
            if c > 25:
                f = f + d * 1.0 / c * 5.0 - e * 1.0 / c * 5.0
            else:
                f = f + d * 0.2 - e * 0.2
            score[countIndex] = f
            countIndex += 1
        scoreDict['genericScore'] = score[0]
        scoreDict['graphicScore'] = score[1]
        scoreDict['soundScore'] = score[2]
        scoreDict['actorScore'] = score[3]
        new_score = root.child('movies/'+movieKey).update(scoreDict)
            # print(countPosComment)
            # print(countNegComment)
    except KeyError:
        print("no comment")
        continue
