from database.Database import *
from database.MySQLDataSource import *

class DateDao(object):
    def __init__(self, db):
        self.__db = db
        self.__tableName = "date"
        self.__fieldId = "ID_Date"
        self.__lastId = db.getMaxId(self.__tableName, self.__fieldId) + 1
    def addDate(self, row):
        res = self.__db.insert(self.__tableName, [self.__lastId] + row)
        print("fghjkl", res)
        if res == 1:
            self.__lastId += 1
            print("bien")
            return self.__lastId - 1
        print("mal")
        return 0
    def findIdDate(self, keyword):
        res = self.__db.selectIdEqual(self.__tableName, self.__fieldId, "Date", keyword)
        if res == None: return 0
        return res[1][0] if len(res) == 2 else 0