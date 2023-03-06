from database.Database import *
from database.MySQLDataSource import *


# Classe PostDAO contient le nom de la table Post ainsi que l'Id de la table
# et aussi les fonction addPost pour ajouter un post
class PostDao(object):
    def __init__(self, db):
        self.__db = db
        self.__tableName = "post"
        self.__fieldId = "ID_Post"
        self.__lastId = db.getMaxId(self.__tableName, self.__fieldId) + 1
    def addPost(self, row):
        res = self.__db.insert(self.__tableName, [self.__lastId] + row)
        if res == 1:
            self.__lastId += 1
            print("post bien")
            return self.__lastId - 1
        print("post mal")
        return 0