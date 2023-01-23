from database.MySQLDataSource import *


class Database(object):
    def __init__(self, dataSource = None):
        self.setDataSource(dataSource)

    def setDataSource(self, dataSource):
        if dataSource != None :
            self.__dataSource = dataSource
            self.__db = dataSource.getConnection()
            if self.__db.is_connected():
                print("connection ...")
        else :
            self.__db = None

    def getConnection(self):
        try :
            if self.__db.is_connected(): return
        except :
            self.__db.close()
        self.__db = self.__dataSource.getConnection()

    def insert(self, tableName, row):
        try:
            if not self.__db.is_connected():
                self.getConnection()
            cursor = self.__db.cursor()
            ind = ''
            query = "INSERT INTO " + tableName + " VALUES ("
            for i in range(0, len(row)):
                query += ind + "%s"
                ind = ', '
            query += ")"
            if tableName == 'post' : print(row)
            cursor.execute(query, tuple(row))
            res = cursor.rowcount
            print(cursor.rowcount, "Record inserted successfully into authors table")
            cursor.close()
            return res

        except Exception as error:
            print("Failed to insert record into " + tableName + "table {}".format(error))
            return 0

    def executeSelect(self, query):
        try:
            if not self.__db.is_connected():
                self.getConnection()
            cursor = self.__db.cursor()
            cursor.execute(query)
            result = [[i[0] for i in cursor.description]]
            cols = cursor.fetchall()
            for x in cols:
                result.append(list(x))
            cursor.close()
            return result
        except Exception as error:
            print("Failed to select from table ", error.msg)
            return None

    def select(self, tableName):
        query = "SELECT * FROM " + tableName
        return self.executeSelect(query)

    def getMaxId(self, tableName, field):
        query = "SELECT MAX(" + field + ") FROM " + tableName
        print(query)
        res = self.executeSelect(query)
        if res == None : return 0
        else : return int(res[1][0]) if res[1][0] != None else 1

    def selectIdEqual(self, tableName, idField, field, keyword):
        query = "SELECT " + idField + " FROM " + tableName + " WHERE " + field + " LIKE '" + keyword + "'"
        print(query)
        return self.executeSelect(query)

