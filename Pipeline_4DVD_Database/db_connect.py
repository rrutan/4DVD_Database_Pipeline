import mysql.connector
from mysql.connector import Error
import pandas as pd
import os
import time

# pip install mysql-connector-python== 8.0.16

def connect_to_mysql(user, password, host, database):
    """
    Connect to a MySQL database using mysql-connector.

    Args:
        user (str): Username for the database.
        password (str): Password for the database.
        host (str): Host address (e.g., "localhost").
        database (str): Name of the database to connect to.

    Returns:
        connection: A MySQL connection object if successful, None otherwise.
    """
    try:
        connection = mysql.connector.connect(
            user=user,
            password=password,
            host=host,
            database=database,
            allow_local_infile = True
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def table_to_csv(connection, table_names=["Date","Lat","Lon","Gridbox"], output_dir = "./data/db_structure"):
    """
    Export existing MySql Table to csv to guide data processing, if not already downloaded. 

    Args:
        connection: MySQL.connector connection object
        table_names (list): List of tables names to export from db, default ["Date","Lat","Lon","Gridbox"]
        output_dir (str): Path the folder to save csv
    
    Returns:
        tables_dict: Dictionary of table names and values of dataframes, guides conversion of data before insert
    """
    
    os.makedirs(output_dir, exist_ok=True)
    tables_dict = {}

    try:
        for table_name in table_names:

            query = f"SELECT * FROM {table_name};"
            data = pd.read_sql(query, connection)


            file_path = os.path.join(output_dir, f"{table_name}.csv")
            data.to_csv(file_path, index = False)
            print(f"Table: {table_name} written to {file_path}")

            # add to dict
            tables_dict[table_name.lower()] = data

        return tables_dict

    except Exception as e:
        print(f"Failed to export {table_name}: {e}")



def close_connection(connection):
    """
    Close the MySQL database connection.

    Args:
        connection: A MySQL connection object.
    """
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")

def csv_to_database(connection, csv_file_path, table_name):
    """
    Load processsed data from csv to database

    Args:
        connection: MySQL.connector connection object.
        csv_file (str): path the csv of data.
        table_name (str): Name of table to insert into.
        batch_n (int): Number of rows to insert in a batch, default 10,000

    Return:
        None
    """
    
    try:
        cursor = connection.cursor()
        query = f"""
            LOAD DATA LOCAL INFILE '{os.path.abspath(csv_file_path)}'
            INTO TABLE {table_name}
            FIELDS TERMINATED BY ','
            ENCLOSED BY '"'
            LINES TERMINATED BY '\\n'
            IGNORE 1 LINES;
        """

        start_time = time.time()
        cursor.execute(query)
        connection.commit()
        end_time = time.time()

        print(f"Data from {csv_file_path} inserted into {table_name} in {end_time-start_time:.2f} seconds")

    except mysql.connector.Error as e:
        print(f"Error during data load: {e}")
        connection.rollback()
    finally:
        cursor.close()
        print('Connection closed')
