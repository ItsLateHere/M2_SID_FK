from database.Database import *
from database.MySQLDataSource import *

class ReactionDao(object):
    def __init__(self, db):
        self.__db = db
        self.__tableName = "reaction"
        self.__fieldId = "ID_Reaction"
        self.__lastId = db.getMaxId(self.__tableName, self.__fieldId) + 1
    def addReaction(self, row):
        res = self.__db.insert(self.__tableName, [self.__lastId] + row)
        print("fghjkl", res)
        if res == 1:
            self.__lastId += 1
            print("bien")
            return self.__lastId - 1
        print("mal")
        return 0