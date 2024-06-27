import sys
import requests
from models import Station, Installation
from typing import List

BASEURL = "https://api.gios.gov.pl/pjp-api/rest/station"


class UnsuccessfulRequestException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


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
            response = requests.get(f"{self.base_url}/findAll")
            response.raise_for_status()
            response_json = response.json()
        except requests.exceptions.RequestException as e:
            raise UnsuccessfulRequestException(f"Error requesting data: {e}") from None

        stations_list = [
            Station(station.get("id"), station.get("stationName"))
            for station in response_json
            if "id" in station and "stationName" in station
        ]
        return stations_list

    def get_installations_of_station(self, station_id: int) -> List[Installation]:
        """
        Fetches all installations for a specific station.
        :param station_id: Station ID.
        :return: List of all installations for specific station.
        """
        try:
            response = requests.get(f"{self.base_url}/sensors/{station_id}")
            response.raise_for_status()
            response_json = response.json()
        except requests.exceptions.RequestException as e:
            raise UnsuccessfulRequestException(f"Error requesting data: {e}") from None

        installations_list = [
            Installation(
                installation.get("id"), installation.get("param", {}).get("paramCode")
            )
            for installation in response_json
            if "id" in installation
            and "param" in installation
            and "paramCode" in installation.get("param", {})
        ]
        return installations_list
