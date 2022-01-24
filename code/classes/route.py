# -----------------------------------------------------------
# route.py
#
# Class definition of a Route object
# A Route consists of Station and Connection objects, 
# forming a route 
#
# Authors: Sam Bijhouwer and Maik Larooij
# -----------------------------------------------------------

class Route():
    """ 
    Represents a route, consisting of station objects and connection objects, forming a route

    Arguments:
    - max_time: the max. total time of the route in minutes, for Holland max_time = 120, for Nationaal max_time = 180
    - start_station (optional): enables the option to create a route from a starting station
    """

    def __init__(self, max_time, start_station=None):
        self.stations = []
        self.connections = []
        self.total_time = 0
        self.max_time = max_time

        if start_station:
            self.add_station(start_station, start_station)

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
        """ 
        Retrieves new candidates for the route, where candidates can be neighbors of either the first or last station in the route.
        Candidates must not exceed the max time and must not already exist in route.
        """
        candidates = [(station, neighbor, distance) for station in [self.stations[0], self.stations[-1]]
                                                        for neighbor, distance in station.neighbors.items()
                                                        if self.total_time + distance < self.max_time and
                                                        neighbor not in self.stations]

        return list(set(candidates))

    def calc_score(self, graph_connections):
        """ 
        Calculates the score of the route according to the formula:
        K = P*10000 - M
        
        P = Fraction of all connections included in routemap
        M = Total time of all routes in minutes
        """

        # Calculate total time of all routes
        self.M = self.total_time

        # Calculate number of stations and number of routes
        self.P = len(self.connections) / graph_connections

        # Calculate final score
        score = (self.P * 10000) -  self.M

        return score

    def copy(self):
        """
        Creates a deepcopy of self
        """
        new_route = Route(self.max_time)

        new_route.connections = self.connections.copy()
        new_route.stations = self.stations.copy()
        new_route.total_time = self.total_time

        return new_route
        
    def __str__(self):
        return f"{[station for station in self.stations]}"

    def __repr__(self):
        return f"{[station for station in self.stations]}"