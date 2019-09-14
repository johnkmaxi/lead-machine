import configparser
import psycopg2
from sql_queries import tables, columns

def create_database(conn_info, db='POSTGRES', schema=None):
    """Deletes the lead-machine database

    Parameters
    ----------
    conn_info : str
        File path to config file with database connection info
    db : str
        Header in configfile. Name of database to get parameters for. E.g.,
        POSTRES, ORACLE
    schema : None, optional
        Defaults to 'leadmachine'.
    """
    # connect to default database
    config = configparser.ConfigParser()
    config.read(conn_info)
    host = config[db]['host']
    #port = int(config[db]['port'])
    #service_name = config[db]['service_name']
    dbname = config[db]['dbname']
    username = config[db]['username']
    password = config[db]['password']
    conn = psycopg2.connect(f"host={host} dbname={dbname} user={username} password={password}")
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    if schema is None:
        schema = 'leadmachine'

    # create sparkify database with UTF8 encoding
    cur.execute(f"DROP DATABASE IF EXISTS {schema}")
    cur.execute(f"CREATE DATABASE {schema} WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to default database
    conn.close()

    # # connect to sparkify database
    # conn = psycopg2.connect(f"host={host} dbname={dbname} user={username} password={password}")
    # cur = conn.cursor()
    #
    # return cur, conn

def delete_database(conn_info, db='POSTGRES', schema=None):
    """Deletes the lead-machine database

    Parameters
    ----------
    conn_info : str
        File path to config file with database connection info
    db : str
        Header in configfile. Name of database to get parameters for. E.g.,
        POSTRES, ORACLE
    schema : None, optional
        Defaults to 'leadmachine'.
    """
    # connect to default database
    config = configparser.ConfigParser()
    config.read(conn_info)
    host = config[db]['host']
    #port = int(config[db]['port'])
    #service_name = config[db]['service_name']
    dbname = config[db]['dbname']
    username = config[db]['username']
    password = config[db]['password']
    conn = psycopg2.connect(f"host={host} dbname={dbname} user={username} password={password}")
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    if schema is None:
        schema = 'leadmachine'

    # delete lead machine database with UTF8 encoding
    cur.execute(f"DROP DATABASE IF EXISTS {schema}")

    # close connection to default database
    conn.close()

def drop_tables(conn): #, drop_table_queries
    drop_query = """DROP TABLE IF EXISTS {};"""
    for table in tables:
        print(drop_query.format(table))
        conn.cursor().execute(drop_query.format(table))
        conn.commit()


def create_tables(conn): #, create_table_queries, columns
    create_query = """CREATE TABLE IF NOT EXISTS {} {};"""
    for table in tables:
        print(create_query.format(table, columns[table]))
        conn.cursor().execute(create_query.format(table, columns[table]))
        conn.commit()

def main():
    # cur, conn = create_database()
    #
    # drop_tables(cur, conn)
    # create_tables(cur, conn)
    #
    # conn.close()
    pass


if __name__ == "__main__":
    main()
