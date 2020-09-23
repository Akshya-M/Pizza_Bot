from mysql.connector import connect, errorcode, Error


def ConnectMySql(table_name):
    try:
        mydb = connect(
            host="localhost", user="root", password="root", database=table_name,
        )
        return mydb
    except Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return False
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return False
        else:
            print(err)
            return False