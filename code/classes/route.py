# -----------------------------------------------------------
# route.py
#
# Class definition of a Route object
# A Route consists of Station and Connection objects, 
# forming a route 
#
# Authors: Mijntje Meijer, Sam Bijhouwer and Maik Larooij
# -----------------------------------------------------------

class Route():
    def __init__(self, max_time):
        self.stations = []
        self.connections = []
        self.total_time = 0
        self.max_time = max_time

    def add_station(self, start, station):
        """
        Adds a station object to the route at the place based on start station
        start = station from which the neighbor is going to get added
        station = station to be added
        """
        # If station is first station, append to list
        if start == station:
            self.stations.append(station)
            return

        # Determine if the origin station is at the start or end of the route
        station_s = [station for station in self.stations if station.name == start.name][0]
        index = self.stations.index(station_s)

        # If at the start, insert new station before origin station. Else, insert new station at the end
        self.stations.insert(0 if index == 0 else index + 1, station)
        
    def add_connection(self, connection):
        """
        Adds a connection object to the route and count up total time
        """
        self.connections.append(connection)
        self.total_time += connection.distance

    def get_new_options(self):

        candidates = [(station, neighbor, distance) for station in [self.stations[0], self.stations[-1]]
                                                        for neighbor, distance in station.neighbors.items()
                                                        if self.total_time + distance < self.max_time and
                                                        neighbor not in self.stations]

        return candidates

    def __str__(self):
        return f"{[station for station in self.stations]}"