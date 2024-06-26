import sys
import requests
import json
from typing import List, Dict, Any


def request_all_stations(url: str) -> List[Dict[str, str]]:
    """
    Sends GET request to retrieve all stations.

    :param url: URL to fetch stations data from

    :return: Sorted list of dictionaries with keys 'id' and 'name' for each station.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)
            stations_list = [{"id": station["id"], "name": station["stationName"]} for station in data]
            stations_list = sorted(stations_list, key=lambda x: x["id"])
            return stations_list

        elif response.status_code == 429:
            print("Too many requests for all stations!")

        else:
            print(f"Failed to retrieve stations data. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error requesting data: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    sys.exit(1)


def request_all_installations(stations_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Fetches installation data for each station in the provided list.

    :param stations_list: A list of dictionaries, each containing 'id' and 'name' of a station.

    :return:  A list of dictionaries, each containing 'id', 'name', and 'installations' of each station.
    """
    stations_with_installations = []

    for station in stations_list:
        station_id = station["id"]
        station_name = station["name"]
        installations = _fetch_installations_for_station(station_id)

        stations_with_installations.append({
            "id": station_id,
            "name": station_name,
            "installations": installations
        })

    return stations_with_installations


def _fetch_installations_for_station(station_id: int) -> List[Dict[str, Any]]:
    """
    Sends a GET request to retrieve installation data for a given station ID.

    :param station_id: The ID of the station to fetch installation data for.

    :return: A list of dictionaries, each containing 'id' and 'paramCode' of an installation.
    """
    try:
        response = requests.get(f"https://api.gios.gov.pl/pjp-api/rest/station/sensors/{station_id}")
        if response.status_code == 200:
            data = json.loads(response.text)
            installations_list = [
                {"id": installation["id"], "paramCode": installation["param"]["paramCode"]}
                for installation in data
            ]
            return installations_list

        elif response.status_code == 429:
            print("Too many requests for installations!")

        else:
            print(f"Failed to retrieve installations data fo station: #{station_id}."
                  f"Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error requesting data: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")


if __name__ == '__main__':
    print("Fetching data from API, please wait")
    url_request = "https://api.gios.gov.pl/pjp-api/rest/station/findAll"

    all_stations = request_all_stations(url_request)
    stations_with_installations = request_all_installations(all_stations)

    for station in stations_with_installations:
        print(f"Station #{station['id']} ({station['name']}):")
        for installation in station["installations"]:
            print(f"Installation #{installation['id']}: '{installation['paramCode']}'")
        print()
