import sqlite3

import jarpis


class User(object):
    def __init__(self, id, name, speakerID):
        self._id = id
        self._name = name
        self._speakerID = speakerID

    @staticmethod
    def createUserTable():
        connection = sqlite3.connect(jarpis.database)
        c = connection.cursor()

        try:
            c.execute(
                "CREATE TABLE `USER` ( `ID` INTEGER PRIMARY KEY AUTOINCREMENT, `USERNAME` TEXT, "
                "`SPEAKERID` INTEGER UNIQUE )"
            )
        except sqlite3.OperationalError as error:
            print("CREATE TABLE WARNING: {0}").format(error)

        connection.commit()
        connection.close()

    @staticmethod
    def dropUserTable():
        connection = sqlite3.connect(jarpis.database)
        c = connection.cursor()

        try:
            c.execute(
                "DROP TABLE USER"
            )
        except sqlite3.OperationalError as error:
            print("DROP TABLE WARNING: {0}").format(error)

        connection.commit()
        connection.close()

    def insertUser(self):
        connection = sqlite3.connect(jarpis.database)
        c = connection.cursor()

        c.execute(
            "INSERT INTO USER(USERNAME, SPEAKERID) VALUES (?, ?)", (self._name, self._speakerID,)
        )
        connection.commit()
        connection.close()

        return self

    def updateUser(self, name):
        connection = sqlite3.connect(jarpis.database)
        c = connection.cursor()

        c.execute(
            "UPDATE USER SET USERNAME=? WHERE ID=?", (name, self._id)
        )

        connection.commit()
        connection.close()

        return self

    @staticmethod
    def getUserByID(id):
        connection = sqlite3.connect(jarpis.database)
        c = connection.cursor()

        c.execute(
            "SELECT * FROM USER WHERE ID=?", (id,)
        )
        result = c.fetchone()
        connection.close()

        if result is not None:
            return User(result[0], result[1], result[2])

        raise UserNotFoundException("No User with given ID: %d" %id)

    def deleteUser(self):
        connection = sqlite3.connect(jarpis.database)
        c = connection.cursor()

        c.execute(
            "DELETE FROM USER WHERE ID=?", (self._id,)
        )
        connection.commit()
        connection.close()
        return True


class UserNotFoundException(Exception):
    pass