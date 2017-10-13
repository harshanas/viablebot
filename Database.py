import MySQLdb as mdb
import json


class Database:
    def __init__(self):
        self.host = "localhost"
        self.username = "root"
        self.password = ""
        self.database = "Viable"
        self.con = mdb.connect(self.host, self.username, self.password, self.database)

    def add_user(self, sender_id):
        with self.con:
            cur = self.con.cursor()
            cur.execute("INSERT INTO user_table(sender_id) VALUES ("+sender_id+")")

    def is_user_exist(self, sender_id):
        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT * FROM user_table WHERE Sender_ID="+sender_id)
            rows = cur.fetchall()
        if len(rows) > 0:
            return True
        else:
            return False

    def get_store(self, lat, lng):
        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT * FROM store_table WHERE lat = "+lat+" AND lng="+lng)
            rows = cur.fetchall()
        if len(rows) > 0:
            return rows
        else:
            return False




