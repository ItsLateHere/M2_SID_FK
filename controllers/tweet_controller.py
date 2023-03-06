import json
import threading
import time
from datetime import date, datetime
import os

from database import Database, MySQLDataSource

from api.api_twitter import *

from dao.CompteDao import *
from dao.PostDao import *
from dao.ReactionDao import *

# creation une connexion avec la DB 'dbt_twitter'
dataSource = MySQLDataSource("dbt_twitter")

dbC = Database(dataSource)
dbP = Database(dataSource)
dbR = Database(dataSource)

compteDao = CompteDao(dbC)
postDao = PostDao(dbP)
reactionDao = ReactionDao(dbR)

# À partir du fichier JSON, on sauvegarde les tweets dans la base de données transactionnelle
def runSaveInSQL():
    global routeFile
    fileName = routeFile
    fl = open(fileName)
    for line in fl:
        a = json.loads(line)
        idCompte = compteDao.findIdCompte(a['username'])
        if idCompte == 0:
            rowC = [a['username'], a['name'], a['compte_created_at'], a['followers_count'], a['verified'],
                    a['protected']]
            idCompte = compteDao.addCompte(rowC)

        rowR = [date.today(), "", a['like_count'], a['reply_count'], a['retweet_count'], a['quote_count']]
        idReaction = reactionDao.addReaction(rowR)

        rowP = [a['text'], a['url'], a['id_Tweet'], a['is_fake'], a['confidance'],
                a['tweet_created_at'], idCompte, idReaction]
        postDao.addPost(rowP)
    fl.close()
    os.remove(fileName)

# Gérer le lancement de sauvegarde dans la base de données chaque 3 min
def saveInSQL():
    global threadRunSaveInSQL
    time.sleep(60 * 3)
    threadRunSaveInSQL = threading.Thread(target=runSaveInSQL)
    threadRunSaveInSQL.start()

# Récupérer les données  complémentaires à partir de l'API TWITTER et les sauvegarder dans un fichier Json temporaire
def saveInJson(article_list):
    global routeFile
    f = open(routeFile, 'a')
    for a in article_list:
        try :
            user = get_User(a['poster_user_tag'][1:])
            tweet = get_Tweet(a['tweet_id'].split('/')[-1])
            post = {**user, **tweet,
                    'url': 'https://twitter.com/' + user['username'] + '/statuses/' + str(tweet['id_Tweet']),
                    'confidance': float(a['msg_res'][13:19]), "is_fake": a["is_fake"]}
            json.dump(post, f)
            f.write("\n")
        except : None
    f.close()

# cette fonction gère l'écriture dans le fichier JSON et relance les threads pour la sauvegarde dans la base de données
def saveTweets(article_list):
    global threadSaveInSQL, threadRunSaveInSQL, routeFile
    #si le thread de sauvegarde dans la DB, il est en cours d'attendre le lancement sauvegarde dans la DB
    if threadSaveInSQL.is_alive():
        if threadRunSaveInSQL != None: # si le thread de sauvegarde ç'a été lancer et terminer
            init()
    if not threadSaveInSQL.is_alive():
        init()
    saveInJson(article_list)

# initialisation de thread qui est responsable au lancement de sauvegarde dans la DB ainsi que la création du fichier temporaire JSON
def init():
    global threadSaveInSQL, threadRunSaveInSQL, routeFile

    threadSaveInSQL = threading.Thread(target=saveInSQL)
    threadSaveInSQL.start()
    threadRunSaveInSQL = None
    routeFile = "tempData/" + datetime.now().strftime("%d%m%Y%H%M%S") + "tweets" + ".json"
    f = open(routeFile, 'a')
    f.close()

init()
