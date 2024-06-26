import sys
import requests
import json
from typing import Optional, List
from dataclasses import dataclass, field

STATIONS_URL = "https://api.gios.gov.pl/pjp-api/rest/station/findAll"
INSTALLATIONS_URL = "https://api.gios.gov.pl/pjp-api/rest/station/sensors/"


@dataclass
class Installation:
    """
    A class to represent an installation.

    Attributes:
        id (int): ID of the installation.
        param_code (str): Parameter code of the installation.
    """
    id: int
    param_code: str

    def __str__(self):
        return f"Installation: #{self.id}: '{self.param_code}'"


@dataclass
class Station:
    """
    A class to represent a Station.

    Attributes:
        id (int): ID of the Station.
        name (str): Name of the Station
        installations (List[Installation]): A list of all installations.
    """
    id: int
    name: str
    installations: Optional[List] = field(default_factory=list)

    def __str__(self):
        installations_str = '\n'.join(str(installation) for installation in self.installations)
        return f"Station #{self.id} ({self.name}):\n{installations_str}"


class ApiHandler:
    """
    A class to handle API calls.
    Attributes:
        stations_url (str): URL to get all the stations
        installations_url (str): URL to get all the installations for specific station
    """
    def __init__(self, stations_url: str = STATIONS_URL, installations_url: str = INSTALLATIONS_URL):
        self.stations_url = stations_url
        self.installations_url = installations_url

    def get_all_stations(self) -> List[Station]:
        """
        Fetches all stations from the API.
        :return: A List of all stations.
        """
        try:
            response = requests.get(self.stations_url)
            if response.status_code == 200:
                data = json.loads(response.text)
                stations_list = [Station(station["id"], station["stationName"]) for station in data]
                return stations_list

            elif response.status_code == 429:
                print("Too many requests for all stations!")

            else:
                print(f"Failed to retrieve stations data. Status code: {response.status_code}")

        except KeyError as e:
            print(f"Problem with finding key in JSON: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Error requesting data: {e}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        sys.exit(1)

    def sort_stations(self, stations: List[Station]) -> List[Station]:
        """
        Sorts list of stations by their ID.
        :param stations: List of all stations.
        :return: Sorted list of all stations.
        """
        return sorted(stations, key=lambda station: station.id)

    def get_installations_of_station(self, station_id: int) -> List[Installation]:
        """
        Fetches all installations for a specific station.
        :param station_id: Station ID.
        :return: List of all installations for specific station.
        """
        try:
            response = requests.get(f"{self.installations_url}{station_id}")
            if response.status_code == 200:
                data = json.loads(response.text)
                return [Installation(installation["id"], installation["param"]["paramCode"]) for installation in data]

            elif response.status_code == 429:
                print("Too many requests for installations!")

            else:
                print(f"Failed to retrieve installations data fo station: #{station_id}."
                      f"Status code: {response.status_code}")

        except KeyError as e:
            print(f"Problem with finding key in JSON: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Error requesting data: {e}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")


if __name__ == "__main__":
    print("Fetching data from API, please wait")
    handler = ApiHandler()
    stations = handler.get_all_stations()
    stations = handler.sort_stations(stations)

    for station in stations:
        station.installations = handler.get_installations_of_station(station.id)

    for station in stations:
        print(station, end="\n\n")
