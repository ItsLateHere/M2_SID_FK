import mysql.connector
# La classe MySQLDataSource il fait la connexion avec la base de données MySQL
# pour que l'application puisse de sauvegarder les données dans la base de données transactionnelles
class MySQLDataSource(object):
    __host =  "83.115.75.78"
    __user = "fk"
    __password = "fk"
    def __init__(self, databaseName = ""):
        self.__databaseName = databaseName

    def getConnection(self):
        if self.__databaseName != "":
            try:
                connection = mysql.connector.connect(
                    host = self.__host,
                    database = self.__databaseName,
                    user = self.__user,
                    password = self.__password
                )
                print('connecion database ' + self.__databaseName + " ...")
                return connection
            except mysql.connector.Error as error:
                print("Failed to connect on database : " + self.__databaseName)
                return None

        else :
            print("Name of the database wasn't declared")
            return None
    @property
    def databaseName(self):
        return self.__databaseName

    @databaseName.setter
    def databaseName(self, databaseName):
        self.__databaseName = databaseName


