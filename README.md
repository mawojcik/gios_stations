# Air Quality Stations Data Fetcher

This Python script retrieves all air quality monitoring stations and their installations from the [GIOŚ API]( http://powietrze.gios.gov.pl/pjp/content/api) and displays details to standard output.

## Requirements

- Python 3.x
- `requests` library

## Usage

1. **Setup**

   - Ensure Python 3.x is installed on your system.
   - Install the required `requests` library using pip:
     ```
     pip install requests
     ```

2. **Running the Script**

   - Clone the repository or download `main.py`, `models.py`, `api_handler.py` file.
   - Navigate to the directory containing the script.
   - Run the script using Python:
     ```
     python3 main.py
     ```
   - The script will fetch data from the GIOŚ API and display station details along with their installations.
