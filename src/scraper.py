"""Crawler classes for scraping web data

"""

import configparser
import psycopg2

class BaseCrawler:
    """Collects information from web-based sources and stores to database

    Parameters
    ----------
    source : str
        A URL indicating the where the crawler should begin data collection
    conn_info : str
        A filepath to a config file with database connection information

    Attributes
    ----------
    conn : psycopg2 connection object

    Methods
    -------
    make_connection(conn_info)
    to_db(query)

    """
    def __init__(self, source=None, conn_info=None):
        self.conn = self.make_connection(conn_info)
        self.conn.set_session(autocommit=True)

    def make_connection(self, conn_info, db='POSTGRES'):
        """Returns a connection to database

        Parameters
        ----------
        conn_info : str
            A filepath to a config file with database connection information

        Returns
        -------
        conn : psycopg2 connection object
        """
        if conn_info is None: # use default db on local host
            conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=postgres")
        else: # parse the config file and connect
            config = configparser.ConfigParser()
            config.read(conn_info)
            host = config[db]['host']
            #port = int(config[db]['port'])
            #service_name = config[db]['service_name']
            dbname = config[db]['dbname']
            username = config[db]['username']
            password = config[db]['password']
            conn = psycopg2.connect(f"host={host} dbname={dbname} user={username} password={password}")
        return conn

    def to_db(self, query):
        """Writes a query to a database

        Parameters
        ----------
        query : str
        """
