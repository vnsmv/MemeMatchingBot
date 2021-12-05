create_users_table = """
CREATE TABLE USERS(
   ID INT PRIMARY KEY     NOT NULL,
   NAME           TEXT    NOT NULL,
   AGE            INT,
   DESCR        CHAR(50)
);
"""

create_memes_table = """
CREATE TABLE memes(
   ID SERIAL PRIMARY KEY,
   TG_ID INT UNIQUE NOT NULL,
   AUTHOR_ID    INT   NOT NULL,
   CREATE_DATE TIMESTAMP,
   CONSTRAINT meme_author
      FOREIGN KEY(AUTHOR_ID)
        REFERENCES USERS(ID)
);
"""

create_users_users_table = """
CREATE TABLE users_users(
   ID  SERIAL PRIMARY KEY,
   USER_ID INT NOT NULL,
   REC_USER_ID    INT   NOT NULL,
   REACTION BOOLEAN NOT NULL,
   DATE TIMESTAMP,
   CONSTRAINT act_user
      FOREIGN KEY(USER_ID)
        REFERENCES USERS(ID),
   CONSTRAINT rec_user
      FOREIGN KEY(REC_USER_ID)
        REFERENCES USERS(ID)
);
"""

create_users_memes_table = """
CREATE TABLE users_memes(
   ID  SERIAL PRIMARY KEY,
   USER_ID INT NOT NULL,
   MEMES_ID INT NOT NULL,
   REACTION INT NOT NULL,
   DATE TIMESTAMP,
   CONSTRAINT user_const
      FOREIGN KEY(USER_ID)
        REFERENCES USERS(ID),
   CONSTRAINT meme_const
      FOREIGN KEY(MEMES_ID)
        REFERENCES MEMES(ID)
);
"""

def add_user(connection, cursor, name, age=None, desc=None):
    query = """
    INSERT INTO USERS(NAME, AGE, DESCR)
    VALUES (%s, %s, %s)
    """
    try:
        cursor.execute(query, vars=(name, age, desc))
    except Exception as e:
        print(e)
        cursor.execute("ROLLBACK")
    connection.commit()

def add_meme(connection, cursor, tg_id, author_id, date=None):
    query = """
    INSERT INTO MEMES(TG_ID, AUTHOR_ID, CREATE_DATE)
    VALUES (%s, %s, %s)
    """
    try:
        cursor.execute(query, vars=(tg_id, author_id, date))
    except Exception as e:
        print(e)
        cursor.execute("ROLLBACK")
    connection.commit()

def add_user_user_reaction(connection, cursor, act_user, rec_user, reaction, date=None):
    query = """
    INSERT INTO users_users(USER_ID, REC_USER_ID, REACTION, DATE)
    VALUES (%s, %s, %s, %s)
    """
    try:
        cursor.execute(query, vars=(act_user, rec_user, reaction, date))
    except Exception as e:
        print(e)
        cursor.execute("ROLLBACK")
    connection.commit()

def add_user_meme_reaction(connection, cursor, user_id, memes_id, reaction, date=None):
    query = """
    INSERT INTO users_memes(USER_ID, MEMES_ID, REACTION, DATE)
    VALUES (%s, %s, %s, %s)
    """
    try:
        cursor.execute(query, vars=(user_id, memes_id, reaction, date))
    except Exception as e:
        print(e)
        cursor.execute("ROLLBACK")
    connection.commit()

