import sqlite3


class SQLite_db():
    """
    This class make a 'req' requests to sqlite database with 'args' arguments.
    """

    def __init__(self, db):
        self.con = sqlite3.connect(db, check_same_thread=False)
        self._zip = ['id', 'sex', 'name', 'age', 'sex_partner', 'age_partner_from', 'age_partner_to', 'meeting_id']

    def check(self, req, args=None) -> tuple:
        if args is None:
            args = []
        cur = self.con.cursor()
        cur.execute(req, args)
        res = cur.fetchone()
        cur.close()
        return res

    def checkall(self, req, args=None) -> list:
        if args is None:
            args = []
        cur = self.con.cursor()
        cur.execute(req, args)
        res = cur.fetchall()
        cur.close()
        return res

    def query(self, req, args=None):
        if args is None:
            args = []
        cur = self.con.cursor()
        cur.execute(req, args)
        self.con.commit()
        cur.close()

    def querymany(self, req, args=None):
        if args is None:
            args = []
        cur = self.con.cursor()
        cur.executemany(req, args)
        self.con.commit()
        cur.close()

    def to_model(self, args: tuple, model):
        return model(**dict(zip(self._zip, args)))
