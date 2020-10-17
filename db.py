import json

import psycopg2
from psycopg2.extras import RealDictCursor

import conf


def main():
    conn = psycopg2.connect(dbname=conf.pg_database, user=conf.pg_login,
                            password=conf.pg_password, host=conf.pg_host)
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    rq = """
            BEGIN TRAN 'text'  
                   INSERT INTO users (username, password, email) VALUES ('abc', '{password}', '{email}');  
            ROLLBACK TRAN 'text';  
    """.format(name="abc", password="bca", email="qwerty@mail.ru")

    a = cursor.execute(rq)

    # cursor.execute('''CREATE TABLE users (
    #     id SERIAL PRIMARY KEY,
    #     username VARCHAR ( 50 ) UNIQUE NOT NULL,
    #     password VARCHAR ( 50 ) NOT NULL,
    #     email VARCHAR ( 255 ) UNIQUE NOT NULL
    # );''')
    #
    # for i in range(1, 21):
    #     rq = "INSERT INTO users (username, password, email) VALUES ('user{0}', 'password{0}', 'user{0}@pochta.com')".format(str(i))
    #     cursor.execute(rq)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
