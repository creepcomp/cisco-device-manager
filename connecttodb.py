import sqlite3
from settings import *


def getdevicefromid(rowIDrow):

    try:
        sqliteConnection = sqlite3.connect(dbfile)
        cursor = sqliteConnection.cursor()

        query = f"SELECT * FROM devices WHERE id = {rowIDrow}"
        cursor.execute(query)
        record = cursor.fetchall()
        for row in record:
            retid = row[0]
            retname = row[1]
            retip = row[2]
            retusername = row[3]
            retpassword = row[4]
            retdescription = row[5]
            rettype = row[6]
            retgolden = row[7]

        return (
            retid,
            retname,
            retip,
            retusername,
            retpassword,
            retdescription,
            rettype,
            retgolden,
        )

    except sqlite3.Error as error:
        pass
