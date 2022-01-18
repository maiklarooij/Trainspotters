# -----------------------------------------------------------
# connection.py
#
# Class definition of a Connection object
# A connection consists of two Station objects and a distance
#
# Authors: Mijntje Meijer, Sam Bijhouwer and Maik Larooij
# -----------------------------------------------------------

class Connection():
    """
    Represents a connection between two stations.
    """
    def __init__(self, station1, station2, distance):
        self.station1 = station1
        self.station2 = station2
        self.distance = distance

    def __repr__(self):
        return f"{self.station1} to {self.station2}. Distance {self.distance}"