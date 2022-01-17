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
    def __init__(self):
        self.stations = []
        self.connections = []
        self.total_time = 0

    def add_station(self, station, time):
        """
        Adds a station object to the route and increases total time of the route
        """
        self.stations.append(station)
        self.total_time += time

    def add_connection(self, connection):
        """
        Adds a connection object to the route
        """
        self.connections.append(connection)

    def __str__(self):
        return f"{[station for station in self.stations]}"