class Connection():
    def __init__(self, station1, station2, distance):
        self.station1 = station1
        self.station2 = station2
        self.distance = distance

    def __repr__(self):
        return f"{self.station1} to {self.station2}. Distance {self.distance}"