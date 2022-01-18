import psycopg2

from memeder.database.config import host, database, user, password, host_test, database_test, user_test, password_test


def connect_to_db(test=False):
    if test:
        connection = psycopg2.connect(host=host_test, database=database_test, user=user_test, password=password_test)
    else:
        connection = psycopg2.connect(host=host, database=database, user=user, password=password)
    cursor = connection.cursor()
    return cursor, connection
