class Route():
    def __init__(self):
        self.stations = []
        self.connections = []
        self.total_time = 0

    def add_station(self, start, station, time):
        self.total_time += time
        if start == station:
            self.stations.append(station)
            return
        
        index = self.stations.index(start)
        if index == 0:
            self.stations.insert(0, station)
        else:
            self.stations.append(station)
        

    def add_connection(self, connection):
        self.connections.append(connection)

    def __str__(self):
        return f"{[station for station in self.stations]}"