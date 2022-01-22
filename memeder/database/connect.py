import os

from dotenv import load_dotenv
import psycopg2

from memeder.paths import get_py_lib_path


def connect_to_db(env_file=None):
    if env_file is None:
        pass
        # loading env variables from heroku env
    elif env_file in ('db_credentials.env', 'db_credentials_test.env'):
        load_dotenv(get_py_lib_path() / 'database' / env_file)
    else:
        raise ValueError(f'`env_file` should be one of the '
                         f'(`None`, `db_credentials.env`, `db_credentials_test.env`). '
                         f'However, {env_file} is given.')

    host = os.environ.get('DATABASE_HOST')
    database = os.environ.get('DATABASE_DATABASE')
    user = os.environ.get('DATABASE_USER')
    password = os.environ.get('DATABASE_PASSWORD')

    connection = psycopg2.connect(host=host, database=database, user=user, password=password)
    cursor = connection.cursor()

    return cursor, connection
