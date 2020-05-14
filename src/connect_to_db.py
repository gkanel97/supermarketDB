import mysql.connector
from mysql.connector import Error
from configparser import ConfigParser

def read_db_config(filename="database.ini", section="mysql"):

    """ Read database configuration file and return a dictionary object
        filename: name of the configuration file
        section: section of database configuration """

    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to mysql
    config_dict = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            config_dict[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return config_dict

def connect():
    db_config = read_db_config()
    conn = None
    try:
        print("Connecting to MySQL database")
        conn = mysql.connector.MySQLConnection(**db_config)

        if conn.is_connected():
            print("Connection established")
            return conn
        else:
            print("Connection failed")

    except Error as error:
        print(error)

def disconnect(conn):
    if conn is not None and conn.is_connected():
        conn.close()
        print("Connection closed")
