import mysql.connector

from utils.functions import func

config = func.get("utils/config.json")
global mydb

def createConnection(db):
    global mydb
    mydb = mysql.connector.connect(
        host=config.mysql_host,
        user=config.mysql_user,
        passwd=config.mysql_pass,
        database=db,
        port=config.mysql_port
    )
    return mydb

def Init():
    rows = []
    db_list = ["devolution", "devolution_economy", "devolution_warnings", "devolution_leveling", "devolution_blacklisted"]
    mydb = mysql.connector.connect(
        host=config.mysql_host,
        user=config.mysql_user,
        passwd=config.mysql_pass,
        port=config.mysql_port
    )
    mycursor = mydb.cursor(buffered=True)
    for db in db_list:
        mycursor.execute(f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{db}'")
        for Row in mycursor:
            rows.append("".join(Row))
    for db in db_list:
        if not db in rows:
            mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {db}")
            print(f"Generating Database: {db}")

def db_check(db):
    mydb = mysql.connector.connect(
        host=config.mysql_host,
        user=config.mysql_user,
        passwd=config.mysql_pass,
        port=config.mysql_port
    )
    mycursor = mydb.cursor(buffered=True)

    mycursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(db.replace('\'', '\'\'')))

    if mycursor.fetchone()[0] == 1:
        mycursor.close()
        return True

def tableCheck(db, table):
    createConnection(db)
    mycursor = mydb.cursor(buffered=True)

    mycursor.execute(f"SELECT count(*) FROM information_schema.TABLES WHERE (TABLE_SCHEMA = '{db}') AND (TABLE_NAME = '{table}')")

    if mycursor.fetchone()[0] == 1:
        mycursor.close()
        return True

def Entry_Check(Check, Row, DB, Table):
    cur = mydb.cursor(buffered=True)
    query = (f"SELECT {Row} FROM `{DB}`.`{Table}`")
    cur.execute(query)

    for Row in cur:
        if Check in Row:
            cur.close()
            return True

def Fetch(Row, DB, Table, Where, Value):
    table = str.maketrans(dict.fromkeys("()"))
    cur = mydb.cursor()
    query = (f"SELECT {Row} FROM `{DB}`.`{Table}` WHERE {Where} = {Value}")
    cur.execute(query)
    row = str(cur.fetchone())
    return row.translate(table)
