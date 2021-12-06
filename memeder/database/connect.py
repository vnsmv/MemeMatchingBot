import psycopg2
from memeder.database.config import host, database, user, password

def connect_to_db():
    connection = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password)

    cursor = connection.cursor()
    return cursor, connection



