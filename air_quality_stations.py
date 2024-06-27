import sys
import requests
from typing import Optional, List
from dataclasses import dataclass, field

BASEURL = "https://api.gios.gov.pl/pjp-api/rest/station/"


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
        if self.installations == []:
            installations_str = "No installations found"
        else:
            installations_str = '\n'.join(str(installation) for installation in self.installations)
        return f"Station #{self.id} ({self.name}):\n{installations_str}"


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


if __name__ == "__main__":
    print("Fetching data from API, please wait")
    handler = ApiHandler()
    stations = handler.get_all_stations()
    stations = sorted(stations, key=lambda station: station.id)

    for station in stations:
        station.installations = handler.get_installations_of_station(station.id)

    for station in stations:
        print(station, end="\n\n")
