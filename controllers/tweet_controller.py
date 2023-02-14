import json
import threading
import time
from datetime import date, datetime
import os

from database import Database, MySQLDataSource

from api.api_twitter import *

from dao.CompteDao import *
# from dao.DateDao import *
from dao.PostDao import *
from dao.ReactionDao import *
from dao.SubjectDao import *
from dao.ZoneGeoDao import *

dataSource = MySQLDataSource("dbt_twitter")

dbC = Database(dataSource)
# dbD = Database(dataSource)
dbP = Database(dataSource)
dbR = Database(dataSource)
dbS = Database(dataSource)
dbZ = Database(dataSource)

compteDao = CompteDao(dbC)
# dateDao = DateDao(dbD)
postDao = PostDao(dbP)
reactionDao = ReactionDao(dbR)
subjectDao = SubjectDao(dbS)
zoneGeoDao = ZoneGeoDao(dbZ)


def runSaveInSQL():
    global routeFile
    fileName = routeFile
    fl = open(fileName)
    for line in fl:
        a = json.loads(line)
        # {"idCompte": 416529990, "name": "Khadija", "username": "khad_ij", "compte_created_at": "2023-02-13 12:57:31",
        #  "protected": false, "verified": false, "location": "Royaume du Maroc", "followers_count": 12289,
        #  "text": "Bonjour. Question existentielle pourquoi il nya plus de moutarde au McDo ?",
        #  "idTweet": 1625116962073325568, "geo": null, "retweet_count": 3, "reply_count": 40, "like_count": 59,
        #  "quote_count": 4, "url": "https://twitter.com/khad_ij/statuses/1625116962073325568", "confidance": 100.0,
        #  "is_fake": 0}

        idCompte = compteDao.findIdCompte(a['username'])
        if idCompte == 0:
            # ID_Compte, username, name, date_creation, handle, NB_followers, verifcation, protected
            rowC = [a['username'], a['name'], a['compte_created_at'], a['followers_count'], a['verified'],
                    a['protected']]
            idCompte = compteDao.addCompte(rowC)

        rowR = [date.today(), "", a['like_count'], a['reply_count'], a['retweet_count'], a['quote_count']]
        idReaction = reactionDao.addReaction(rowR)

        # ID_Post, text, URL, ID_externe_tweet, classe,confidence,date,
        # ID_Subject,ID_Compte,ID_Reaction, ID_Zone_geo
        rowP = [a['text'], a['url'], a['id_Tweet'], a['is_fake'], a['confidance'],
                a['tweet_created_at'], 0, idCompte, idReaction, 0]
        idPost = postDao.addPost(rowP)
    fl.close()
    os.remove(fileName)


def saveInSQL():
    global threadRunSaveInSQL
    time.sleep(30)
    threadRunSaveInSQL = threading.Thread(target=runSaveInSQL, args=())
    threadRunSaveInSQL.start()


def saveInJson(article_list):
    global routeFile
    print(routeFile)
    f = open(routeFile, 'a')
    for a in article_list:
        user = get_User(a['poster_user_tag'][1:])
        print(user)
        tweet = get_Tweet(a['tweet_id'].split('/')[-1])
        print(tweet)
        post = {**user, **tweet,
                'url': 'https://twitter.com/' + user['username'] + '/statuses/' + str(tweet['id_Tweet']),
                'confidance': float(a['msg_res'][13:19]), "is_fake": a["is_fake"]}
        json.dump(post, f)
        f.write("\n")
    f.close()


def saveTweets(article_list):
    global threadSaveInSQL, threadRunSaveInSQL, routeFile
    if threadSaveInSQL.is_alive():
        if threadRunSaveInSQL != None:
            init()
    if not threadSaveInSQL.is_alive():
        init()
    saveInJson(article_list)


def init():
    global threadSaveInSQL, threadRunSaveInSQL, routeFile

    threadSaveInSQL = threading.Thread(target=saveInSQL)
    threadSaveInSQL.start()
    threadRunSaveInSQL = None
    print("zzzz")
    routeFile = "tempData/" + datetime.now().strftime("%d%m%Y%H%M%S") + "tweets" + ".json"


init()
