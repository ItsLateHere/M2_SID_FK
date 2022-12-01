# import mysql.connector
# Classify the tweet

# CRUD Operations on transactional DB


# def insertAutor(Au_ID, Author, Year_Born):
#     try :
#         connection = mysql.connector.connect(host='localhost', database = 'Biblio', user = 'root', password='')
#
#         cursor = connection.cursor()
#         mySql_insert_query = """INSERT INTO authors (Au_ID, Author, Year_Born) VALUES (%s, %s, %s) """
#         record = (Au_ID, Author, Year_Born)
#         cursor.execute(mySql_insert_query, record)
#         connection.commit()
#         print(cursor.rowcount, "Record inserted successfully into authors table")
#         cursor.close()
#
#     except mysql.connector.Error as error:
#         print("Failed to insert record into authors table {}".format(error))
#
#     finally:
#         if connection.is_connected():
#             connection.close()
#             print("MySQL connection is closed")