class Station():
    def __init__(self, name, coord):
        self.name = name
        self.coord = coord
        self.neighbors = {}

    def add_neighbor(self, neighbor, distance):
        """
        Adds a neighbor to the station with the distance to that station.
        """
        self.neighbors[neighbor] = distance

    def __str___(self):
        return f"{self.name}:{self.coord}"

    def __repr__(self):
        return f"Station {self.name}"