# 4DVD Database Pipeline

## Overview

The **4DVD Database Pipeline** is a Python-based tool for processing, converting, and inserting gridded climate data into a MySQL database. It supports extracting, reshaping, and managing data efficiently while maintaining compatibility with an existing database schema. This tool is ideal for integrating large datasets into a structured database for further analysis or visualization.

---

## Features

- **Data Loading**: Fetches climate data in NetCDF format, either by downloading it from a specified URL or reading it locally.
- **Data Conversion**: Processes NetCDF datasets into CSV files, conforming to the structure of an existing database.
- **Database Integration**: Efficiently inserts large datasets into a MySQL database, avoiding duplication of existing records.
- **Table Export**: Exports MySQL database tables (e.g., Date, Lat, Lon, Gridbox) to CSV for use in data processing.
- **Batch Processing**: Handles large datasets using batch operations to ensure scalability.

---

## Project Structure

```
project_root/
|├──4dvd_database_pipeline/
|   |├── __init__.py
|   |├── get_data.py       # Module for loading NetCDF data
|   |├── convert_data.py   # Module for reshaping and exporting data
|   |└── db_connect.py     # Module for database interaction
|├──test_functions.py      # Script for testing pipeline functionality
|├── data/                 # Folder for raw and processed data
|├── docs/                 # Documentation folder
|├── requirements.txt      # Python dependencies
|├── setup.py              # Package installation script
|├── README.md             # Project documentation
|└── LICENSE.txt           # License information
```

---

## Installation

### Prerequisites

- **Python**: Version 3.8 or higher.
- **MySQL**: A running instance of MySQL or MariaDB.

### Steps

1. Clone the repository:

   ```bash
   git clone <repository-url> **IN PROGRESS**
   cd 4dvd_database_pipeline
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Loading and Processing Data

1. **Load NetCDF Data**:

   ```python
   from 4dvd_database_pipeline import get_data
   dataset = get_data.load_data(download=False, file_path='data/sst.mnmean.nc')
   ```

2. **Export Database Tables**:

   ```python
   from 4dvd_database_pipeline import insert_data
   connection = insert_data.connect_to_mysql(user="root", password="", host="localhost", database="ersst")
   insert_data.export_tables_to_csv(connection, output_dir='data/db_structure')
   ```

3. **Process Data for Database**:

   ```python
   from 4dvd_database_pipeline import convert_data
   tables_dict = convert_data.load_existing_tables()
   processed_df = convert_data.process_gridded_data(dataset, var_name='sst', tables_dict=tables_dict)
   ```

4. **Insert Data into Database**:

   ```python
   from 4dvd_database_pipeline import insert_data
   insert_data.csv_to_database(connection, csv_file_path='data/processed/gridded_data.csv', table_name='gridded_data')
   ```

5. **Close Database Connection**:
   ```python
   insert_data.close_connection(connection)
   ```

### Running Tests

To test functionality, use the provided `test_functions.py`:

```bash
python test_functions.py
```

---

## Configuration

### Database Settings

Modify the database connection parameters in your script:

```python
user = "root"
password = "your_password"
host = "localhost"
database = "your_database"
```

### File Paths

Ensure all file paths (e.g., for CSV and NetCDF files) are correctly set relative to the project directory.

---

## Dependencies

- Python (>= 3.8)
- pandas
- mysql-connector-python
- xarray

See `requirements.txt` for a complete list.

---

## License

This project is licensed under the MIT License. See `LICENSE.txt` for details.

---

## Acknowledgments

Special thanks to the SDSU Climate Informatics Lab for their guidance and support in developing this pipeline.
This README file was partially created with the assistance of ChatGPT by OpenAI.
