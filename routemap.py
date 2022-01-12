import csv
import random

def load_data(scale = 'Holland'):
    """ 
    Load in the necessary .csv files. Options: 
    scale = 'Holland' or 'Nationaal'
    """
    with open(f"data/Connecties{scale}.csv", mode="r") as file:
        connections_csv = list(csv.reader(file))
    
    with open("data/StationsHolland.csv", mode="r") as file:
        stations_csv = list(csv.reader(file))

    return {'connections': connections_csv, 'stations': stations_csv}

# Define max route time and total stations
MAX_ROUTE_TIME = 120
SCALE = 'Holland'
TOTAL_STATIONS = len(load_data(scale = SCALE)['stations'])

class Connection:
    """ Object which represents a connection """
    def __init__(self, origin, destination, distance):
        self.origin = origin
        self.destination = destination
        self.distance = distance

    def __str__(self):
        return f"{self.origin} to {self.destination}: {self.distance}"


class Route:
    """ Object which represents multiple connections, forming a route """
    def __init__(self):
        self.connections = []
        self.stations = set()

    def add_connection(self, connection):
        """Adds a connection to the route if the total distance does not exceed 120 minutes"""
        if sum(c.distance for c in self.connections) + connection.distance > MAX_ROUTE_TIME:
            return False
        else:
            self.connections.append(connection)
            self.stations.add(connection.origin)
            self.stations.add(connection.destination)
            return True

    def __str__(self):
        return ", ".join(str(connection) for connection in self.connections)


class Routemap:
    """ Object which represents all routes, forming a routemap """
    def __init__(self, amount):
        self.routes = {i:Route() for i in range(amount)}
        self.stations = set()
    
    def print_solution(self):
        for i, route in self.routes.items():
            print(f"Route #{i}: ")
            t_time = 0
            for connection in route.connections:
                t_time += connection.distance
                print(connection)
            print(f"Total Route time: {t_time}\n")
        
        print(f"Score of routemap: {self.calc_score()}")

    def calc_score(self):
        Min = 0
        for route in self.routes.values():
            for connection in route.connections:
                Min += connection.distance
        
        score = 10000 - (len(self.routes) * 100 + Min)

        return score

    def generate_output(self):
        """ Writes the output to a .csv file """

        header = ['train', 'stations']
        footer = ['score', self.calc_score()]

        # Create a new file
        with open("output.csv", mode='w', newline='') as output_file:
            writer = csv.writer(output_file)

            writer.writerow(header)

            # Retrieve stations from all routes and write them to the file
            for i, route in self.routes.items():
                writer.writerow([f'train_{i+1}', list(route.stations)])

            writer.writerow(footer)


# Get the necessary data
connections_csv, stations_csv = (load_data(scale = SCALE)['connections'],
                                load_data(scale = SCALE)['stations'])

# Create a routemap and add connections
test = Routemap(7)
for line in connections_csv[1:]:
    c = Connection(line[0], line[1], int(line[2]))
    while True:
        random_route = random.randint(0, 6)
        if test.routes[random_route].add_connection(c):
            break

test.print_solution()
test.calc_score()
test.generate_output()
