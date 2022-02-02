# -----------------------------------------------------------
# graph.py
#
# Class definition of a Graph object
# A Graph contains Station and Connection objects, forming
# a graph from .csv files. The Graph is used in algorithms
#
# Authors: Sam Bijhouwer and Maik Larooij
# -----------------------------------------------------------

import csv
from src.classes.connection import Connection
from src.classes.station import Station


class Graph:
    """
    Represents a graph, with stations as nodes and connections as edges.

    Arguments:
    - stations_file: a csv file containing the stations
    - connections_file: a csv file containing the connections
    - scale: the scale of the graph, either 'Holland' or 'Nationaal'
    """

    def __init__(self, stations_file, connections_file, scale):
        self.total_connections = 0
        self.stations = self.load_stations(stations_file)
        self.connections = self.load_connections(connections_file)
        self.scale = scale
        self.MAX_TIME, self.MAX_ROUTES = self.get_constants()

    def load_stations(self, stations_file):
        """
        Adds stations from source file into the graph.
        """
        stations = {}

        with open(stations_file, 'r') as s_file:
            reader = csv.DictReader(s_file)

            for row in reader:
                name = row['station']
                coord = (float(row['x']), float(row['y']))
                stations[name] = Station(name, coord)

        return stations

    def load_connections(self, connections_file):
        """
        Adds connections from source file into the graph.
        Also adds neighbors to station objects in graph.
        """
        connections = []

        with open(connections_file, 'r') as c_file:
            reader = csv.DictReader(c_file)

            for row in reader:

                # Add station objects from stations in graph
                station1 = self.stations[row['station1']]
                station2 = self.stations[row['station2']]
                distance = float(row['distance'])

                connections.append(Connection(station1, station2, distance))

                # Add neighbors to stations
                self.stations[row['station1']].add_neighbor(station2, distance)
                self.stations[row['station2']].add_neighbor(station1, distance)

        self.total_connections = len(connections)

        return connections

    def fetch_connection(self, start_station, end_station):
        """
        Given two station objects, return the connection object of the two stations.
        """
        targets = (start_station, end_station)

        # Search connection object of the two target stations
        connection = [connection for connection in self.connections if connection.station1 in targets and connection.station2 in targets]

        # Return connection if found
        if connection:
            return connection[0]

        return None

    def get_constants(self):
        """
        Determine constants based on the scale.
        """
        if self.scale == "Holland":
            MAX_TIME = 120
            MAX_ROUTES = 7
        elif self.scale == "Nationaal":
            MAX_TIME = 180
            MAX_ROUTES = 20

        return MAX_TIME, MAX_ROUTES
