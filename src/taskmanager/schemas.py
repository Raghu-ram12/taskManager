import sqlite3

DB_PATH = "app.db"


def get_connection():
    """Use this everywhere in your app to open a connection."""
    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA foreign_keys = ON")  
    return connection


def init_db(connection):
    
    try:

        cursor = connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS USERS (
                USER_ID     INTEGER PRIMARY KEY,
                FIRST_NAME  VARCHAR(50),
                SECOND_NAME VARCHAR(50),
                EMAIL       TEXT UNIQUE NOT NULL
                            CHECK (EMAIL LIKE '%@%.%' AND LENGTH(EMAIL) >= 5)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS TASKS (
                TASK_ID      INTEGER PRIMARY KEY,
                USER_ID      INTEGER NOT NULL,
                TASK_NAME    TEXT UNIQUE NOT NULL,
                TASK_STATUS  TEXT DEFAULT 'NOT STATED',
                PRIORITY     INTEGER CHECK (PRIORITY > 0 AND PRIORITY <= 5),
                DIFFICULTY   TEXT CHECK (DIFFICULTY IN ('LOW', 'MEDIUM', 'HIGH')),
                CREATED_DATE TEXT DEFAULT CURRENT_TIMESTAMP,
                DEADLINE     TEXT,
                FOREIGN KEY (USER_ID) REFERENCES USERS(USER_ID)
            )
        ''')

        connection.commit()

        

    except sqlite3.Error as e:
        connection.rollback()
        print(f"Database error: {e}")
        raise  # stop the app if the DB can't be set up

    