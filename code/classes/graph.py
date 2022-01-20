# -----------------------------------------------------------
# graph.py
#
# Class definition of a Graph object
# A Graph contains Station and Connection objects, forming
# a graph from .csv files. The Graph is used in algorithms
#
# Authors: Mijntje Meijer, Sam Bijhouwer and Maik Larooij
# -----------------------------------------------------------

import csv

from .station import Station
from .connection import Connection

class Graph():
    def __init__(self, stations_file, connections_file):
        self.stations = self.load_stations(stations_file)
        self.connections = self.load_connections(connections_file)

    def load_stations(self, stations_file):
        """ 
        Adds stations from source file into the graph 
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

        return connections

    def fetch_connection(self, start_station, end_station, new_station):
        """ 
        Given two station objects, return the connection object of the two stations
        """
        connection = [connection for connection in self.connections if (connection.station1 in (new_station, start_station) and connection.station2 in (new_station, start_station)) 
        or (connection.station1 in (new_station, end_station) and connection.station2 in (new_station, end_station))]

        if connection:
            return connection[0]

        return None 

