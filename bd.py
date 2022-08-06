import sqlite3, datetime

class DataBase:
    def __init__(self, dbname="db.sqlite3"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def find(self, date):
        stmt = "SELECT * FROM hb WHERE date=(?)"
        args = (date, )
        return self.conn.execute(stmt, args).fetchall()
    def update(self, id):
        stmt = "UPDATE hb SET date=(?) WHERE id=(?)"
        datenow = datetime.datetime.now()
        datenextyear =  datetime.datetime(datenow.year+1, datenow.month, datenow.day).strftime('%d.%m.%Y')
        args = (datenextyear, id)
        self.conn.execute(stmt, args)
        self.conn.commit()