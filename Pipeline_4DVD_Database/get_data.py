import xarray as xr
import os, requests

    
dataset_urls = { ##  this is subject to change over time, can add more as needed
    "ersst": "https://downloads.psl.noaa.gov/Datasets/noaa.ersst.v5/sst.mnmean.nc"
}
    
def download_data(data_name, output_dir = "./data/raw"):
    """
    Download a dataset from a predefined URL and save it locally. 

    args:
        data_name (str): Name of dataset to download (ex: "ersst, ...)
        output_dir (str): Directory where data is downloaded to.

    returns:
        str: Path to downloaded file
    """
    if data_name not in dataset_urls:
        raise ValueError(f"Dataset '{data_name}' not available, add to dictionary if necessary")
    
    url = dataset_urls[data_name]

    # make sure ouput dir if it doesnt already exist
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{data_name}.nc")
    
    try:
        response = requests.get(url, stream = True)
        response.raise_for_status()

        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size = 1024):
                f.write(chunk)
        
        print(f"Downloaded {data_name} to {output_path}")
        return output_path
    
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to download")

def load_data(file_path= None, download = False, data_name = None, output_dir = "./data/raw", data_var = 'sst'):
    """
    Load a NetCDF file locally or downloaded from the web using netCDF.Dataset.

    args:
        file_path (str): Path to local NetCDF file, default None.
        download (bool): Whether or not to download the dataset, default False.
        data_name (str): Name of dataset to download, default None.
        ouput_dir (str): Directory to put downloaded file, default 'data' dir
        data_var (str): Variable to load from NetCDF to dataset, default 'sst'

    Returns:
        netCDF.Dataset: The loaded NetCDF dataset
    """
    if download ==True:
        if not data_name:
            raise ValueError("Please specify a dataset to download")
        file_path = download_data(data_name=data_name, output_dir=output_dir)

    if not file_path or not os.path.exists(file_path):
        raise FileNotFoundError("The NetCDF file doesnt exist.")

    try: 
        dataset_all = xr.open_dataset(file_path, engine='netcdf4')
        dataset = dataset_all[['lat','lon','time',data_var]]
        print(f"NetCDF file loaded: {file_path}")
        return dataset
    except Exception as e:
        raise RuntimeError(f"Error Loading NetCDF file: {e}")
