import sqlite3

class DB:
    def __init__(self,username):
        self.user = username
        self.connection = sqlite3.connect("dohamdam/db.sqlite3")
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS dohamdam (
            "id" INTEGER NOT NULL,
            "user" TEXT NOT NULL,
            "person_id" text NOT NULL,
            "number_of_tries" INTEGER NOT NULL,
            "is_left" INTEGER NOT NULL,
            "created_at" TEXT NOT NULL,
            "updated_at" TEXT,
            PRIMARY KEY ("id")
        )''')
        self.connection.commit()

    def insert(self, person_id, is_left, number_of_tries=1):
        self.cursor.execute(f'''insert into dohamdam (user, person_id, is_left, number_of_tries, created_at) VALUES
        ({self.user},{person_id},{is_left},{number_of_tries},datetime('now'))
        ''')
        self.connection.commit()

    def exist(self,person_id):
        return self.cursor.execute(f'''SELECT EXISTS(
            SELECT id from dohamdam where user="{self.user}" AND person_id="{person_id}"
        )''').fetchone() == (1,)

    def __del__(self):
        self.connection.close()