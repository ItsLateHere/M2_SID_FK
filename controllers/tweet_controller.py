import json
import threading
import time
from datetime import date, datetime
import os

from database import Database, MySQLDataSource

from dao.CompteDao import *
from dao.DateDao import *
from dao.PostDao import *
from dao.ReactionDao import *
from dao.SubjectDao import *
from dao.ZoneGeoDao import *

dataSource = MySQLDataSource("dbt_twitter")

dbC = Database(dataSource)
dbD = Database(dataSource)
dbP = Database(dataSource)
dbR = Database(dataSource)
dbS = Database(dataSource)
dbZ = Database(dataSource)

compteDao = CompteDao(dbC)
dateDao = DateDao(dbD)
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
        idCompte = compteDao.findIdCompte(a['poster_user_tag'])
        if idCompte == 0:
            rowC = [a['poster_user_tag'], '', '', '', '']
            idCompte = compteDao.addCompte(rowC)
        idDate = dateDao.findIdDate(a['date_time_post'])
        if idDate == 0:
            idDate = dateDao.addDate([a['date_time_post']])
        rowR = [date.today(), "", a['nbr_like'], a['nbr_comment'], a['nbr_retweet']]
        idReaction = reactionDao.addReaction(rowR)
        rowP = [a['tweet_text'], '', 0,
                a['is_fake'], a['msg_res'],
                0, idDate, idCompte, idReaction, 0]
        idPost = postDao.addPost(rowP)
    fl.close()
    os.remove(fileName)


def saveInSQL():
    global threadRunSaveInSQL
    time.sleep(60 * 1)
    threadRunSaveInSQL = threading.Thread(target=runSaveInSQL, args=())
    threadRunSaveInSQL.start()


def saveInJson(article_list):
    global routeFile
    print(routeFile)
    f = open(routeFile, 'a')
    for a in article_list:
        a['poster_user_tag'] = a['poster_user_tag'][1:-1]
        a['date_time_post'] = a['date_time_post'][:10]
        a['tweet_text'] = a['tweet_text'].strip()
        a['msg_res'] = float(a['msg_res'][13:19])

        try:
            a['nbr_like'] = int(a['nbr_like'])
        except:
            a['nbr_like'] = 0

        try:
            a['nbr_comment'] = int(a['nbr_comment'])
        except:
            a['nbr_comment'] = 0

        try:
            a['nbr_retweet'] = int(a['nbr_retweet'])
        except:
            a['nbr_retweet'] = 0

        a.pop('display_id')
        a.pop('poster_user')
        json.dump(a, f)
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
