import Pipeline_4DVD_Database as pipe
    
if __name__ == '__main__':
    
    #Running the line below will download a file of about 100MB
    print("Testing dload of netcdf data from NOAA from get_data.py")
    ds = pipe.load_data(download=True, data_name = 'ersst',output_dir='data/raw', data_var='sst')


    ## Can uncomment the lines below if the netcdf data is already available locally
    # print("Testing loading local data, no download")
    #ds2 = pipe.load_data(download=False, file_path = './data/raw/sst.mnmean.nc')

    # Load database table to get structure from local files
    print("Testing gettting db structure from local files")
    dict1 = pipe.load_existing_tables(date_csv='./data/db_structure/Date_old.csv',
                                      lat_csv='./data/db_structure/Lat_old.csv',
                                      lon_csv='./data/db_structure/Lon_old.csv',
                                      gridbox_csv='./data/db_structure/GridBox_old.csv')

    #This is a test of the database in my local mysql created from a dump file of 4DVD database (replica)
    """
    print("Testing getting db structure from mysql connection")
    
    # connect to db
    conn = pipe.connect_to_mysql(user='root',
                                 password='', 
                                 host='localhost',
                                 database='ersst')
    """

    # download csvs of db structure and load them into a dict, uncomment this if dont have table csvs locally
    #dict2 = pipe.table_to_csv(conn)

    # load a dataframe of the processed data and save it as a csv to data/processed folder 
    print("Testing processing data from netcdf to csv to match db structure")
    processed_data = pipe.process_gridded_data(dataset = ds, var_name = 'sst', tables_dict = dict1)

    # insert csv into table 
    """
    pipe.csv_to_database(conn, 
                         csv_file_path= './data/processed/gridded_data.csv', 
                         table_name='GridData')

    ## I saw that the import worked by visually inspecting the GridData table through mysql gui 
    
    pipe.close_connection(conn)
    """