# -----------------------------------------------------------
# station.py
#
# Class definition of a Station object
# A Station has a name, coordinates and stores neighbors
#
# Authors: Sam Bijhouwer and Maik Larooij
# -----------------------------------------------------------


class Station:
    """
    Represents a single station, for example station Amsterdam Centraal.

    Arguments:
    - name: the name of the station (e.g. Amsterdam Centraal)
    - coord: the x and y coordinates of the station
    """

    def __init__(self, name, coord):
        self.name = name
        self.coord = coord
        self.neighbors = {}

    def add_neighbor(self, neighbor, distance):
        """
        Adds a neighbor to the station with the distance to that station.
        Neighbors are stored in the form neighbor: distance to neighbor (dict).
        """
        self.neighbors[neighbor] = distance

    def __repr__(self):
        """
        Representation of object when printed in list/dict/set.
        """
        return self.name
