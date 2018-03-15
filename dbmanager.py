import MySQLdb

def dbConnect():
    database = MySQLdb.connect( host = "localhost", user = "root", passwd = "", db = "bachelor")
    cursor = database.cursor()

def fetchUsername():
    query ="""SELECT uname FROM users"""