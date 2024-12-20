import pandas as pd

def load_existing_tables(date_csv, lat_csv,lon_csv, gridbox_csv):
    """
    Load in existing tables from the database if already available in local csvs

    Args:
        date_csv (str): Path to date table csv
        lat_csv (str): Path to lat table csv
        lon_csv (str): Path to lon table csv
        gridbox_csv (str): Path to gridbox csv
        Paths to existing tables in the data folder are default

    Returns:
        dict: Dictionary of Dataframes of all tables
    """
    try:
        lon_df = pd.read_csv(lon_csv)
        date_df = pd.read_csv(date_csv)
        lat_df = pd.read_csv(lat_csv)
        gridbox_df = pd.read_csv(gridbox_csv)

        dict = {"date":date_df,
                "lat":lat_df,
                "lon":lon_df,
                "gridbox":gridbox_df}
        print("Existing Tables Loaded")
        return dict
    
    except FileNotFoundError as e:
        raise RuntimeError(f"Error loading tables: {e}")

def process_gridded_data(dataset, var_name, tables_dict, output_csv_path = './data/processed/gridded_data.csv'):
    """
    Get data out of netcdf format and reshape it to a database that 
    matches the gridded_data table in the 4DVD database with 
    existing structure of lat, lon, date, gridbox tables. 

    Args:
        dataset (netCDf4.Dataset): xarray dataset provided by load_data()
        var_name (str): Varaible name to extract ('sst' for ersst dataset)
        tables_dict (dict): Dictionary of dataframes of existing tables in database

    Returns:
        pd.DataFrame: The gridded data table
    """
    # convert nc.dataset to dataframe and replace col names to match db
    df = dataset.to_dataframe()
    df.reset_index(inplace=True)

    df.rename(columns={
        'lat': 'Lat',
        'lon': 'Lon',
        'time': 'Date',
        var_name: 'Value'
    }, inplace=True)

    # get dataframe of ids from tables 
    lats_df = tables_dict['lat']
    lons_df = tables_dict['lon']
    dates_df = tables_dict['date']
    grids_df = tables_dict['gridbox']


    ## Merge all lat, lon, date and gridbox values with thier unique ids
    df_wlats = pd.merge(df, lats_df, on='Lat')

    #problem with Lons, the lon_ID table from the db goes from 0 to 180 then -178 to -2, but the lons in my new df go from 0 360
    #Ill have to convert values that are over 180, subtract 360

    df_wlats["Lon"] = df_wlats['Lon'].apply(lambda x: x-360 if x> 180 else x)

    df_wlatlon = pd.merge(df_wlats, lons_df, on= 'Lon', how = 'left')

    # convert date to string instead of dt object
    df_wlatlon['Date'] = df_wlatlon['Date'].dt.strftime('%Y-%m-%d')

    df_merge = pd.merge(df_wlatlon,dates_df,on="Date",how='left')

    ## Comment out this code if you want to put the most up to date data in the db, I am doing this to only
    ## insert historical data that was missing without changing date bounds 
    df_merge = df_merge.dropna(subset=["Date_ID"])
    
    df_all = pd.merge(df_merge, grids_df, on = ['Lat_ID','Lon_ID'], how = 'left')
    
    cols = ['GridBox_ID','Date_ID','Value']
    grid_data = df_all[cols]

    grid_data.to_csv(output_csv_path, index = False)

    print('netcdf converted to dataframe and saved to csv')
    return grid_data














