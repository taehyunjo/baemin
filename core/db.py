from sqlalchemy import create_engine
from sqlalchemy import MetaData

import config

class db_machine():

    def __init__(self):
        self.host = config.DATABASE_CONFIG['host']
        self.port = config.DATABASE_CONFIG['port']
        self.user = config.DATABASE_CONFIG['user']
        self.pw = config.DATABASE_CONFIG['password']
        self.db_name = config.DATABASE_CONFIG['db_name']

        self.url = 'postgres://' + self.user + ":" + self.pw + "@" + self.host + ":" + self.port + "/" + self.db_name

        self.engine = create_engine(self.url)

    def get_db_table_list(self):
        pass

    def get_db_table(self,table_name):
        pass



