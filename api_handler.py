import sys
import requests
from models import Station, Installation
from typing import List

BASEURL = "https://api.gios.gov.pl/pjp-api/rest/station/"


class ApiHandler:
    """
    A class to handle API calls.
    Attributes:
        base_url (str): prefix of URL to get all the stations/installations
    """
    def __init__(self, base_url: str = BASEURL):
        self.base_url = base_url

    def get_all_stations(self) -> List[Station]:
        """
        Fetches all stations from the API.
        :return: A List of all stations.
        """
        try:
            response = requests.get(self.base_url + "findAll")
            if response.status_code == 200:
                data = response.json()
                stations_list = [
                    Station(station.get("id"), station.get("stationName"))
                    for station in data
                    if "id" in station and "stationName" in station
                ]
                return stations_list

            elif response.status_code == 429:
                print("Too many requests for all stations!")

            else:
                print(f"Failed to retrieve stations data. Status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"Error requesting data: {e}")
        except requests.exceptions.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        sys.exit(1)

    def get_installations_of_station(self, station_id: int) -> List[Installation]:
        """
        Fetches all installations for a specific station.
        :param station_id: Station ID.
        :return: List of all installations for specific station.
        """
        try:
            response = requests.get(f"{self.base_url}sensors/{station_id}")
            if response.status_code == 200:
                data = response.json()
                installations_list = [
                    Installation(
                        installation.get("id"),
                        installation.get("param", {}).get("paramCode")
                    ) for installation in data
                    if "id" in installation and "param" in installation and "paramCode" in installation.get("param", {})
                ]
                return installations_list

            elif response.status_code == 429:
                print("Too many requests for installations!")

            else:
                print(f"Failed to retrieve installations data for station: #{station_id}. "
                      f"Status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"Error requesting data: {e}")
        except requests.exceptions.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
