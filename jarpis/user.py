import sqlite3

conn = None


class User(object):
    def __init__(self, name):
        self._name = name

    @staticmethod
    def createUserTable():
        c = conn.cursor()
        try:
            c.execute(
                "CREATE TABLE `USER` ( `ID` INTEGER PRIMARY KEY AUTOINCREMENT, `USERNAME` INTEGER )"
            )
        except sqlite3.OperationalError as error:
            print("CREATE TABLE WARNING: {0}").format(error)

        conn.commit()

    @staticmethod
    def dropUserTable():
        c = conn.cursor()
        try:
            c.execute(
                "DROP TABLE USER"
            )
        except sqlite3.OperationalError as error:
            print("DROP TABLE WARNING: {0}").format(error)

        conn.commit()

    def insert(self):
        c = conn.cursor()
        c.execute(
            "INSERT INTO USER(USERNAME) VALUES (?)", (self._name,)
        )
        conn.commit()
        return self


class DBUtil():
    result = None

    @staticmethod
    def execute(function, params, production=None):
        global conn
        if production is None:
            production = "test.db"

        conn = sqlite3.connect(production)
        result = function(*params)
        conn.close()

        return result