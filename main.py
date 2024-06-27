from api_handler import ApiHandler

if __name__ == "__main__":
    print("Fetching data from API, please wait")
    handler = ApiHandler()
    stations = handler.get_all_stations()
    stations.sort(key=lambda station: station.id)

    for station in stations:
        station.installations = handler.get_installations_of_station(station.id)
        print(station, end="\n\n")
