

# ### SQL QUERIES TO CREATE NECESSARY TABLES: ###


# ### 1 ###
create_users_table = """
CREATE TABLE users(
   CHAT_ID INT PRIMARY KEY  NOT NULL,
   NAME TEXT NOT NULL,
   USER_BIO TEXT NOT NULL,
   TELEGRAM_ID INT,
   TELEGRAM_USERNAME TEXT,
   DATE_ADD TIMESTAMP,
   IS_FRESH BOOLEAN
);
"""


# ### 2 ###
create_memes_table = """
CREATE TABLE memes(
   ID SERIAL PRIMARY KEY,
   FILE_ID TEXT UNIQUE NOT NULL,
   AUTHOR_ID    INT   NOT NULL,
   CREATE_DATE TIMESTAMP,
   FILE_TYPE TEXT,
   CONSTRAINT meme_author
      FOREIGN KEY(AUTHOR_ID)
        REFERENCES USERS(CHAT_ID)
);
"""


# ### 3 ###
create_users_users_table = """
CREATE TABLE users_users(
   ID  SERIAL PRIMARY KEY,
   USER_ID INT NOT NULL,
   REC_USER_ID    INT   NOT NULL,
   REACTION TEXT NOT NULL,
   DATE TIMESTAMP,
   DATE_REACTION TIMESTAMP,
   MESSAGE_ID INT,
   CONSTRAINT act_user
      FOREIGN KEY(USER_ID)
        REFERENCES USERS(CHAT_ID),
   CONSTRAINT rec_user
      FOREIGN KEY(REC_USER_ID)
        REFERENCES USERS(CHAT_ID)
);
"""


# ### 4 ###
create_users_memes_table = """
CREATE TABLE users_memes(
   ID  SERIAL PRIMARY KEY,
   CHAT_ID INT NOT NULL,
   MEMES_ID INT NOT NULL,
   REACTION TEXT NOT NULL,
   DATE TIMESTAMP,
   DATE_REACTION TIMESTAMP,
   MESSAGE_ID INT NOT NULL,
   CONSTRAINT user_const
      FOREIGN KEY(CHAT_ID)
        REFERENCES USERS(CHAT_ID),
   CONSTRAINT meme_const
      FOREIGN KEY(MEMES_ID)
        REFERENCES MEMES(ID)
);
"""


# ### 5 ###
create_meme_proposals_table = """
CREATE TABLE meme_proposals(
   ID SERIAL PRIMARY KEY,
   CHAT_ID INT NOT NULL,
   MEME_ID INT NOT NULL,
   STATUS INT NOT NULL,
   CONSTRAINT user_const
      FOREIGN KEY(CHAT_ID)
        REFERENCES USERS(CHAT_ID),
   CONSTRAINT meme_const
      FOREIGN KEY(MEME_ID)
        REFERENCES MEMES(ID)
);
"""


# ### 6 ###
create_user_proposals_table = """
CREATE TABLE user_proposals(
   ID SERIAL PRIMARY KEY,
   CHAT_ID INT NOT NULL,
   REC_CHAT_ID INT NOT NULL,
   STATUS INT NOT NULL,
   CONSTRAINT user_const
      FOREIGN KEY(CHAT_ID)
        REFERENCES USERS(CHAT_ID),
   CONSTRAINT rec_user_const
      FOREIGN KEY(REC_CHAT_ID)
        REFERENCES USERS(CHAT_ID)
);
"""


# ### 7 ###
create_top_memes_table = """
CREATE TABLE top_memes(
   MEME_ID INT PRIMARY KEY NOT NULL,
   N_REACTIONS INT NOT NULL,
   AVG_RATING REAL NOT NULL,
   CONSTRAINT meme_const
      FOREIGN KEY(MEME_ID)
        REFERENCES MEMES(ID)
);
"""


def main():
    import argparse
    import logging

    from memeder.database.connect import connect_to_db

    parser = argparse.ArgumentParser()
    parser.add_argument('--force', required=False, action='store_true', default=False)
    parser.add_argument('--test', required=False, action='store_true', default=False)
    args = parser.parse_known_args()[0]

    cursor, connection = connect_to_db(test=args.test)

    force = args.force

    if force:
        # drop_query = "DROP TABLE %s;"
        for table in ("users_memes", "users_users", "memes", "users", ):
            try:
                cursor.execute("DROP TABLE %s;" % table)
            except Exception as e:
                logging.exception(e)
                cursor.execute("ROLLBACK")

    for creating_query in [create_users_table, create_memes_table,
                           create_users_users_table, create_users_memes_table,
                           create_meme_proposals_table, create_user_proposals_table,
                           create_top_memes_table]:
        try:
            cursor.execute(creating_query)
        except Exception as e:
            logging.exception(e)
            cursor.execute("ROLLBACK")

    connection.commit()
    connection.close()


# ### Launch code below to create tables: ###
# ### !!! be careful choosing parameter `force` above !!! ###


if __name__ == '__main__':
    main()
