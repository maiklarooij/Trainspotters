# -----------------------------------------------------------
# routemap.py
#
# Class definition of a Routemap object
# A Routemap consists of Route objects and contains functions 
# to calculate the quality of the lines and generate output
#
# Authors: Sam Bijhouwer and Maik Larooij
# -----------------------------------------------------------

import csv

class Routemap():
    """ 
    Represents a routemap, the end result of an algorithm. Contains the final routes.
    """

    def __init__(self):
        self.routes = []

    def add_route(self, route):
        """ 
        Adds a route object to the routemap
        """
        self.routes.append(route)

    def show_routemap(self):
        """ 
        Prints out the routemap
        """
        for i, route in enumerate(self.routes):
            print(f"Route {i}: {route}. Total time: {route.total_time}")

    def get_total_connections(self):
        """
        Returns the total number of connections in routemap
        """
        all_connections = set()

        for route in self.routes:
            for connection in route.connections:
                all_connections.add(connection)

        return len(all_connections)

    def calc_score(self, graph_connections):
        """ 
        Calculates the score of the routemap according to the formula:
        K = P*10000 - (T*100 + M)
        
        P = Fraction of all connections included in routemap
        T = Number of routes used in routemap
        M = Total time of all routes in minutes
        """

        # Calculate total time of all routes
        self.M = sum([route.total_time for route in self.routes])

        # Calculate number of stations and number of routes
        self.P = self.get_total_connections() / graph_connections
        self.T = len(self.routes)

        # Calculate final score
        score = (self.P * 10000) - (self.T * 100 + self.M)

        return score

    def generate_output(self, graph_connections):
        """ 
        Writes the output to a .csv file 
        """

        header = ['train', 'stations']
        footer = ['score', self.calc_score(graph_connections)]

        # Create a new file
        with open("output.csv", mode='w', newline='') as output_file:
            writer = csv.writer(output_file)

            writer.writerow(header)

            # Retrieve stations from all routes and write them to the file
            for i, route in enumerate(self.routes):
                writer.writerow([f'train_{i+1}', self.routes[i]])

            writer.writerow(footer)

    def copy(self):
        """
        Creates a deepcopy of self
        """
        new_routemap = Routemap()
        new_routemap.routes = self.routes.copy()

        return new_routemap
