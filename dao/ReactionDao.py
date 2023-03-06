from database.Database import *
from database.MySQLDataSource import *

# Classe ReactionDao contient le nom de la table Reaction ainsi que l'Id de la table
# et aussi les fonction addReaction pour ajouter un Reaction
class ReactionDao(object):
    def __init__(self, db):
        self.__db = db
        self.__tableName = "reaction"
        self.__fieldId = "ID_Reaction"
        self.__lastId = db.getMaxId(self.__tableName, self.__fieldId) + 1
    def addReaction(self, row):
        res = self.__db.insert(self.__tableName, [self.__lastId] + row)
        if res == 1:
            self.__lastId += 1
            print("bien")
            return self.__lastId - 1
        print("mal")
        return 0