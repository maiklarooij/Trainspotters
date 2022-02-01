# -----------------------------------------------------------
# connection.py
#
# Class definition of a Connection object
# A connection consists of two Station objects and a distance
#
# Authors: Sam Bijhouwer and Maik Larooij
# -----------------------------------------------------------


class Connection:
    """
    Represents a connection between two stations.

    Arguments:
    - station1: first station object for the connection
    - station2: second station object for the connection
    - distance: distance (in minutes) of the connection
    """

    def __init__(self, station1, station2, distance):
        self.station1 = station1
        self.station2 = station2
        self.distance = distance

    def __repr__(self):
        """
        Representation of object when printed in list/dict/set.
        """
        return f"{self.station1} to {self.station2}. Distance {self.distance}"
