import sqlite3

def readSqliteTableUsers():
    try:
        sqliteConnection = sqlite3.connect('kubera_bank.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_select_query = """SELECT * from users"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        print("Total rows are:  ", len(records))
        print("Printing each row")
        for row in records:
            print("Id: ", row[0])
            print("username: ", row[1])
            print("password", row[2])
            print("fname: ", row[3])
            print("mname: ", row[4])
            print("lname", row[5])
            print("dob: ", row[6])
            print("ssn: ", row[7])
            print("phone", row[8])
            print("email: ", row[9])
            print("\n")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def readSqliteTableChecking():
    try:
        sqliteConnection = sqlite3.connect('kubera_bank.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_select_query = """SELECT * from transactions_checking"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        print("Total rows are:  ", len(records))
        print("Printing each row")
        for row in records:
            print("Id: ", row[0])
            print("username: ", row[1])
            print("date", row[2])
            print("type: ", row[3])
            print("vendor: ", row[4])
            print("amount: ", row[5])
            print("balance", row[5])
            print("\n")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def readSqliteTableSavings():
    try:
        sqliteConnection = sqlite3.connect('kubera_bank.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_select_query = """SELECT * from transactions_savings"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        print("Total rows are:  ", len(records))
        print("Printing each row")
        for row in records:
            print("Id: ", row[0])
            print("username: ", row[1])
            print("date", row[2])
            print("type: ", row[3])
            print("amount: ", row[4])
            print("balance", row[5])
            print("\n")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

readSqliteTableUsers()
readSqliteTableSavings()
readSqliteTableChecking()


