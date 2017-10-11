import MySQLdb as mdb
import json


class Database:
    def __init__(self):
        self.host = "localhost"
        self.username = "root"
        self.password = ""
        self.database = "Grillo"
        self.con = mdb.connect(self.host, self.username, self.password, self.database)

    def add_user(self, sender_id, fname, lname, locale, timezone, gender):
        with self.con:
            cur = self.con.cursor()
            cur.execute("INSERT INTO Users(Sender_ID, FirstName, LastName, Locale, Timezone, Gender) VALUES(%s,%s,%s,%s,%s, %s)",
                        (sender_id, fname, lname, locale, timezone, gender))

    def is_user_exist(self, sender_id):
        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT * FROM Users WHERE Sender_ID="+sender_id)
            rows = cur.fetchall()
        if len(rows) > 0:
            return True
        else:
            return False

    #Bot Specific Functions
    def add_match(self, sender_id, match_data):
        # [{"Unique_id":"1234", "Date":"28/09/2017"}]
        subscribed_matches = self.retrieve_matches(sender_id)
        subscribed_matches = json.loads(subscribed_matches)

        for match in subscribed_matches:
            if match['unique_id'] == match_data['unique_id']:
                return False
        subscribed_matches.append(match_data)
        subscribed_matches = json.dumps(subscribed_matches)
        with self.con:
            cur = self.con.cursor()
            cur.execute("UPDATE Users SET SubscribedMatches = %s WHERE Sender_ID = %s",(subscribed_matches, sender_id))



    def retrieve_matches(self, sender_id):
        with self.con:
            cur = self.con.cursor(mdb.cursors.DictCursor)
            cur.execute("SELECT SubscribedMatches FROM Users WHERE Sender_ID="+sender_id)
            rows = cur.fetchall()
        return rows[0]['SubscribedMatches']

    def add_last_up_time(self, sender_id, match_data):
        last_update_times = self.retrieve_last_up_time(sender_id)
        last_update_times = json.loads(last_update_times)
        last_update_times = last_update_times.append(match_data)
        last_update_times = json.dumps(last_update_times)
        with self.con:
            cur = self.con.cursor()
            cur.execute("UPDATE Users SET LastUpdateTime = %s WHERE Sender_ID = %s",(last_update_times, sender_id))

    def retrieve_last_up_time(self, sender_id, match_name="", singletime=False):
        with self.con:
            cur = self.con.cursor(mdb.cursors.DictCursor)
            cur.execute("SELECT LastUpdateTime FROM Users WHERE Sender_ID="+sender_id)
            rows = cur.fetchall()
            rows = rows[0]["LastUpdateTime"]
        if singletime is True:
            for row in rows:
                if row['MatchName'] == match_name:
                    return row
                    break
        else:
            return rows
    def update_last_up_time(self, sender_id, match_name):
        # [{"MatchName":"Sri Lanka vs India", "Time":"14:00", "NotifyPeriod":"02:00"}]
        return 0
database = Database()
# database.add_user("1234567","Harshana","Dharmawansa","en_US","5.5")
#print(database.is_user_exist("1234567"))
#print(database.is_user_exist("123456"))
# print(database.retrieve_matches("1234567"))
# database.add_match("1234567", {"MatchName":"Sri Lanka vs India", "Date":"28/09/2017", "Time":"00:00"})
#database.add_last_up_time("1234567",{"MatchName":"Sri Lanka vs India", "Time":"14:00", "NotifyPeriod":"02:00"})