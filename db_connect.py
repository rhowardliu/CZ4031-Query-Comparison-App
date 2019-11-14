import psycopg2
import configparser

def get_sql_cursor():
  config = configparser.ConfigParser()
  config.read('./config.ini')
  pg_config = config['postgres']
  return psycopg2.connect(host = pg_config['host'], database = pg_config['database'], \
                           user = pg_config['user'], password = pg_config['password'])

