import connect_to_db
from mysql.connector import Error

def get_one_col(query):
    try:
        conn = connect_to_db.connect()
        cursor = conn.cursor()
        cursor.execute(query)

        col_data = []
        row = cursor.fetchone()
        while row is not None:
            col_data.append(row[0])
            row = cursor.fetchone()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        connect_to_db.disconnect(conn)
        return col_data

def get_table(query):
    try:
        conn = connect_to_db.connect()
        cursor = conn.cursor()
        cursor.execute(query)

        table_data = []
        row = cursor.fetchone()
        while row is not None:
            table_data.append(row)
            row = cursor.fetchone()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        connect_to_db.disconnect(conn)
        return table_data
