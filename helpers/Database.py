import sqlite3


class Database:
    def __init__(self, file: str):
        self.filename: str = file
        self.connection: sqlite3.Connection = sqlite3.connect(file, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.db: sqlite3.Cursor = self.connection.cursor()
        self.execute = self.db.execute
        self.commit = self.connection.commit
        self.execute(
            "CREATE TABLE IF NOT EXISTS keys (id INTEGER PRIMARY KEY AUTOINCREMENT, key TEXT, down INTEGER, time FLOAT)")
        self.execute("CREATE TABLE IF NOT EXISTS mouse_buttons (id INTEGER PRIMARY KEY AUTOINCREMENT, button STRING, "
                     "event STRING, time FLOAT)")
        self.execute(
            "CREATE TABLE IF NOT EXISTS mouse_move (id INTEGER PRIMARY KEY AUTOINCREMENT, x FLOAT, y FLOAT, time FLOAT)")
        self.execute(
            "CREATE TABLE IF NOT EXISTS mouse_wheel (id INTEGER PRIMARY KEY AUTOINCREMENT, delta FLOAT, time FLOAT)")

    def insert(self, table: str, **values):
        rows = ", ".join(i for i in values.keys())
        self.execute(f"INSERT INTO {table} ({rows}) VALUES ({('?, ' * len(values.values()))[:-2]})", tuple(values.values()))
        self.commit()
