# -----------------------------------------------------------
# routemap.py
#
# contains class definitions of objects in the RailNL case:
# connections, routes and routemap
#
# authors: Mijntje Meijer, Sam Bijhouwer and Maik Larooij
# -----------------------------------------------------------

import csv
import random

def load_data(scale = 'Holland'):
    """ 
    Load in the necessary .csv files. Options: 
    scale = 'Holland' or 'Nationaal'
    """

    with open(f"data/Connecties{scale}.csv", mode="r") as file:
        connections_csv = list(csv.reader(file))
    
    with open(f"data/Stations{scale}.csv", mode="r") as file:
        stations_csv = list(csv.reader(file))

    return {'connections': connections_csv, 'stations': stations_csv}

# Define max route time, scale and total stations
MAX_ROUTE_TIME = 120
SCALE = 'Holland'
TOTAL_STATIONS = len(load_data(scale = SCALE)['stations'][1:])

class Connection:
    """ 
    Object which represents a connection
    Has an origin station, a destination station and a distance between the stations
    """

    def __init__(self, origin, destination, distance):

        self.origin = origin
        self.destination = destination
        self.distance = distance

    def __str__(self):
        """ Writes some information about the connection """

        return f"{self.origin} to {self.destination}: {self.distance}"


class Route:
    """ 
    Object which represents multiple connections, forming a route 
    A route consists of a list of connections and a set of connected stations
    """

    def __init__(self):

        self.connections = []
        self.stations = set()

    def add_connection(self, connection):
        """ Adds a connection to the route if the total distance does not exceed 120 minutes """

        if sum(c.distance for c in self.connections) + connection.distance > MAX_ROUTE_TIME:
            return False
        else:
            self.connections.append(connection)

            # Also add origin and destination station of the connection to set of stations
            self.stations.add(connection.origin)
            self.stations.add(connection.destination)

            return True

    def __str__(self):
        """ Writes some information about the connection """

        return ", ".join(str(connection) for connection in self.connections)


class Routemap:
    """ 
    Object which represents all routes, forming a routemap 
    A routemap consists of Route objects
    """
    def __init__(self, amount):
        self.routes = {i:Route() for i in range(amount)}
    
    def print_solution(self):
        """ 
        Writes some information about the routemap
        Printing the connections, total route time and final score
        """

        for i, route in self.routes.items():

            print(f"Route #{i}: ")
            t_time = 0

            for connection in route.connections:
                t_time += connection.distance
                print(connection)

            print(f"Total Route time: {t_time}\n")
        
        print(f"Score of routemap: {self.calc_score()}")

    def calc_score(self):
        """ 
        Calculates the score of the routemap according to the formula:
        K = P*10000 - (T*100 + M)
        
        P = Fractions of all stations included in routemap
        T = Number of routes used in routemap
        M = Total time of all routes in minutes
        """

        # Calculate total time of all routes
        M = 0
        for route in self.routes.values():
            for connection in route.connections:
                M += connection.distance
        
        # Calculate number of stations and number of routes - TODO: maybe make this easier?
        P = len({item for sublist in [list(route.stations) for route in self.routes.values()] for item in sublist}) / TOTAL_STATIONS
        T = len(self.routes)

        # Calculate final score
        score = (P * 10000) - (T * 100 + M)

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
                writer.writerow([f'train_{i+1}', f'[{", ".join(route.stations)}]'])

            writer.writerow(footer)

    def fill_routemap_random(self, connections_data):
        """ Fills the routemap on a random basis """

        for line in connections_data[1:]:
            c = Connection(line[0], line[1], float(line[2]))
            while True:
                random_route = random.randint(0, 6)
                if self.routes[random_route].add_connection(c):
                    break


# Get the necessary data
connections_csv, stations_csv = (load_data(scale = SCALE)['connections'],
                                load_data(scale = SCALE)['stations'])

# Create a routemap and add connections
test = Routemap(7)
test.fill_routemap_random(connections_csv)

test.print_solution()
test.generate_output()
