import sqlite3


class Database:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def is_table_exist(self):
        result = self.cursor.execute("SELECT name FROM sqlite_master where name = 'keys'").fetchone()
        return result is not None

    def create_table(self):
        self.connection.execute("CREATE TABLE keys (key text PRIMARY KEY, status text DEFAULT 'not given')")
        self.connection.commit()

    def number_of_keys(self):
        result = self.cursor.execute('SELECT count(*) FROM keys').fetchone()[0]
        return result

    def has_key(self, key):
        result = self.cursor.execute('SELECT key FROM keys WHERE key = ?', (key,)).fetchone()
        return result is not None

    def is_used(self, key):
        result = self.cursor.execute('SELECT status FROM keys WHERE key = ? and status = "used"', (key,)).fetchone()
        return result is not None

    def add_key(self, key):
        self.connection.execute('INSERT INTO keys VALUES (?, ?)', (key, 'given'))
        self.connection.commit()

    def get_status(self, key):
        result = self.cursor.execute('SELECT status FROM keys WHERE key = ?', (key,)).fetchone()
        return "not given" if result is None else result[0]

    def mark_given(self, key):
        self.connection.execute('UPDATE keys SET status = "given" WHERE key = ?', (key,))
        self.connection.commit()

    def mark_used(self, key):
        self.connection.execute('UPDATE keys SET status = "used" WHERE key = ?', (key,))
        self.connection.commit()

