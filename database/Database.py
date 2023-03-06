from database.MySQLDataSource import *

# Le rôle de la classe Database, c'est d'exécuter le requête SQL comme
# INSERT et SELECT afin d'ajouter ou de récupérer des lignes

class Database(object):
    def __init__(self, dataSource=None):
        self.setDataSource(dataSource)

    def setDataSource(self, dataSource):
        if dataSource != None:
            self.__dataSource = dataSource
            self.__db = dataSource.getConnection()
        else:
            self.__dataSource = None
            self.__db = None

    def executeSelect(self, query):
        try:
            cursor = self.__db.cursor()
            cursor.execute(query)
            myresult = cursor.fetchall()

            result = [[i[0] for i in cursor.description]]
            for x in myresult:
                result.append(list(x))
            return result;
        except mysql.connector.Error as error:
            print("Failed to select from table".format(error))
            return []

    def select(self, tableName):
        query = "SELECT * FROM " + tableName
        return self.executeSelect(query)

    def insert(self, tableName, row):
        try:
            cursor = self.__db.cursor()
            ind = ''
            query = "INSERT INTO " + tableName + " VALUES ("
            for i in range(0, len(row)):
                query += ind + "%s"
                ind = ', '
            query += ")"
            cursor.execute(query, tuple(row))
            self.__db.commit()
            res = cursor.rowcount
            print(cursor.rowcount, "Record inserted successfully into " + tableName + " table")
            cursor.close()
            return res

        except mysql.connector.Error as error:
            print(error)
            print("Failed to insert record into " + tableName + "table {}".format(error))

    def getMaxId(self, tableName, field):
        query = "SELECT MAX(" + field + ") FROM " + tableName;
        res = self.executeSelect(query)
        return int(res[1][0]) if res[1][0] != None else 0

    def selectIdEqual(self, tableName, idField, field, keyword):
        query = "SELECT " + idField + " FROM " + tableName + " WHERE " + field + " = '" + keyword + "'"
        print(query)
        return self.executeSelect(query)
