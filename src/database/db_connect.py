import psycopg2
import configparser


class DB_Manager(object):
    def __init__(self):
        super(DB_Manager, self).__init__()
        config = configparser.ConfigParser()
        config.read('./dbconfig.ini')
        pg_config = config['postgres']
        self.conn = psycopg2.connect(host=pg_config['host'], database=pg_config['database'], user=pg_config['user'], password=pg_config['password'])
        self.cur = self.conn.cursor()
        print('db connection successful')

    def query(self, query):
        print('querying...')
        self.cur.execute(query)
        print('query successful')
        res = self.cur.fetchall()
        return res[0][0][0]
