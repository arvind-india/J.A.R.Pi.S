import sqlite3

conn = None


class User(object):
    def __init__(self, id, name, speakerID):
        self._id = id
        self._name = name
        self._speakerID = speakerID

    @staticmethod
    def createUserTable():
        c = conn.cursor()
        try:
            c.execute(
                "CREATE TABLE `USER` ( `ID` INTEGER PRIMARY KEY AUTOINCREMENT, `USERNAME` TEXT, "
                "`SPEAKERID` INTEGER UNIQUE )"
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

    def insertUser(self):
        c = conn.cursor()
        c.execute(
            "INSERT INTO USER(USERNAME, SPEAKERID) VALUES (?, ?)", (self._name, self._speakerID,)
        )
        conn.commit()
        return self

    def updateUser(self, name):
        c = conn.cursor()
        c.execute(
            "UPDATE USER SET USERNAME=? WHERE ID=?", (name, self._id)
        )
        conn.commit()
        return self

    @staticmethod
    def getUserByID(id):
        c = conn.cursor()
        c.execute(
            "SELECT * FROM USER WHERE ID=?", (id,)
        )
        result = c.fetchone()

        if result is not None:
            return User(result[0], result[1], result[2])

        raise UserNotFoundException("No User with given ID: %d" %id)

    def deleteUser(self):
        c = conn.cursor()
        c.execute(
            "DELETE FROM USER WHERE ID=?", (self._id,)
        )
        conn.commit()
        return True


class UserNotFoundException(Exception):
    pass


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