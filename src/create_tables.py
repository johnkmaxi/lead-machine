import configparser
import psycopg2
from sql_queries import tables, columns

def create_connection(conn_info, db='POSTGRES'):
    """Create a connection to leadmachine

    Parameters
    ----------
    conn_info : str
        File path to config file with database connection info
    db : str
        Header in configfile. Name of database to get parameters for. E.g.,
        POSTRES, ORACLE

    Returns
    -------
    conn : database connection
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
    return conn

def create_database(conn, schema=None):
    """Deletes and recreates leadmachine database

    Parameters
    ----------
    schema : None, optional
        Defaults to 'leadmachine'.
    """
    cur = conn.cursor()
    if schema is None:
        schema = 'leadmachine'

    # create sparkify database with UTF8 encoding
    cur.execute(f"DROP DATABASE IF EXISTS {schema}")
    cur.execute(f"CREATE DATABASE {schema} WITH ENCODING 'utf8' TEMPLATE template0")
    cur.close()

def delete_database(conn, schema=None):
    """Deletes the lead-machine database

    Parameters
    ----------
    conn : psycopg2 connection object

    db : str
        Header in configfile. Name of database to get parameters for. E.g.,
        POSTRES, ORACLE
    schema : None, optional
        Defaults to 'leadmachine'.
    """

    conn.set_session(autocommit=True)
    cur = conn.cursor()
    if schema is None:
        schema = 'leadmachine'

    # delete lead machine database with UTF8 encoding
    cur.execute(f"DROP DATABASE IF EXISTS {schema}")
    cur.close()
    conn.commit()

def drop_table(conn, table):
    drop_query = """DROP TABLE IF EXISTS {};"""
    conn.cursor().execute(drop_query.format(table))
    conn.commit()

def drop_tables(conn): #, drop_table_queries
    drop_query = """DROP TABLE IF EXISTS {};"""
    for table in tables:
        # print(drop_query.format(table))
        conn.cursor().execute(drop_query.format(table))
        conn.commit()

def create_table(conn, table, columns):
    create_query = """CREATE TABLE IF NOT EXISTS {} {};"""
    conn.cursor().execute(create_query.format(table, columns[table]))
    conn.commit()

def create_tables(conn): #, create_table_queries, columns
    create_query = """CREATE TABLE IF NOT EXISTS {} {};"""
    for table in tables:
        #print(create_query.format(table, columns[table]))
        conn.cursor().execute(create_query.format(table, columns[table]))
        conn.commit()

def main():
    conn = create_connection('config.cfg')
    drop_tables(conn)
    delete_database(conn)
    create_database(conn, schema='leadmachine')
    create_tables(conn)


if __name__ == "__main__":
    main()
