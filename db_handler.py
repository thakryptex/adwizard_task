from db_model import Database

"""

Данный класс является обёрткой над db_model для того, чтобы каждый поток непосредственно сам обращался к базе данных.
Каждый метод вызывается из разных потоков, поэтому приходится создавать подключение к БД для каждого отдельного метода.

"""

NAME = "keys.db"


def check_existence():
    db = Database(NAME)
    with db.connection:
        if not db.is_table_exist():
            db.create_table()


def number_of_keys():
    db = Database(NAME)
    with db.connection:
        return db.number_of_keys()


def has_key(key):
    db = Database(NAME)
    with db.connection:
        return db.has_key(key)


def is_used(key):
    db = Database(NAME)
    with db.connection:
        return db.is_used(key)


def add_key(key):
    db = Database(NAME)
    with db.connection:
        db.add_key(key)


def get_status(key):
    db = Database(NAME)
    with db.connection:
        return db.get_status(key)


def mark_given(key):
    db = Database(NAME)
    with db.connection:
        db.mark_given(key)


def mark_used(key):
    db = Database(NAME)
    with db.connection:
        db.mark_used(key)