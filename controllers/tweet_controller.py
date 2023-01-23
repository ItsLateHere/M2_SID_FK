from datetime import date

import database.Database
import database.MySQLDataSource

from dao.CompteDao import *
from dao.DateDao import *
from dao.PostDao import *
from dao.ReactionDao import *
from dao.SubjectDao import *
from dao.ZoneGeoDao import *

dataSource = MySQLDataSource("fk_operationnelle")

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


# db = Database(dataSource)
#
# compteDao = CompteDao(db)
# dateDao = DateDao(db)
# postDao = PostDao(db)
# reactionDao = ReactionDao(db)
# subjectDao = SubjectDao(db)
# zoneGeoDao = ZoneGeoDao(db)

#
import logging
import threading
import time


global threads

threads = list()

def thread_function(article_list):
    for a in article_list:
        idCompte = compteDao.findIdCompte(a['poster_user_tag'][1:-1])
        if idCompte == 0:
            rowC = [a['poster_user_tag'][1:-1], '', '', '', '']
            idCompte = compteDao.addCompte(rowC)
        idDate = dateDao.findIdDate(a['date_time_post'][:10])
        if idDate == 0:
            idDate = dateDao.addDate([a['date_time_post'][:10]])
        rowR = [date.today(), "", a['nbr_like'], a['nbr_comment'], a['nbr_retweet']]
        idReaction = reactionDao.addReaction(rowR)
        rowP = [a['tweet_text'].strip(), '', 0,
                a['is_fake'], float(a['msg_res'][13:19]),
                0, idDate, idCompte, idReaction, 0]
        idPost = postDao.addPost(rowP)

def saveTweets(article_list):
    global threads
    findThreadAlive = False
    for t in threads :
        findThreadAlive = findThreadAlive and t.is_alive()
    if findThreadAlive :
        x = threading.Thread(target=thread_function, args=(article_list,))
        threads.append(x)
    else :
        threads = list()
        x = threading.Thread(target=thread_function, args=(article_list,))
        threads.append(x)
        x.start()
        index = 0
        while index < len(threads):
            thread = threads[index]
            if thread.is_alive():
                thread.join()
            else :
                time.sleep(0.25)
                thread.join()
            if index < len(threads) - 1 :
                threads[index + 1].start()
            index += 1
"""
   try:

poster_user_tag compte : pseudo
date_time_post = date : date
tweet_text = post : text

compte, date, reaction, post

{'display_id': 'id__yg3e5v2y68', done
 'tweet_text': 'Who has the better record: Mbappé or Haaland? ',  done
 'poster_user': 'UEFA Champions League\n@ChampionsLeague\n·\n5 min', done
 'poster_user_tag': '@ChampionsLeague\n', done
  'date_time_post': '2023-01-17T11:13:22.000Z', done
  'nbr_like': '48', 'nbr_comment': '48',  reaction
  'nbr_retweet': '35', 'is_fake': 1, 
  'msg_res': 'is false with 99.85 certainty.'}
"""