class Route():
    def __init__(self):
        self.stations = []
        self.connections = []
        self.total_time = 0

    def add_station(self, station, time):
        self.stations.append(station)
        self.total_time += time

    def add_connection(self, connection):
        self.connections.append(connection)

    def __str__(self):
        return f"{[station for station in self.stations]}"