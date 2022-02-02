# -----------------------------------------------------------
# randomise.py
#
# Class definition to create a random baseline
#
# Authors: Sam Bijhouwer and Maik Larooij
# -----------------------------------------------------------

import random
from src.classes.route import Route
from src.classes.routemap import Routemap


class Random:
    """
    Implements a random algorithm.

    Arguments:
    - graph: the input graph with all stations and connections
    """

    def __init__(self, graph):
        self.graph = graph
        self.routemap = Routemap()

    def run(self):
        """
        Runs the random algorithm
        """
        # Randomly pick a number of routes
        number_of_routes = random.randint(1, self.graph.MAX_ROUTES)

        # Create a routemap object to fill with routes
        routemap = Routemap()

        for _ in range(number_of_routes):

            # Generate a random route and add it to the routemap
            route = generate_random_route(self.graph, 0)
            routemap.add_route(route)

        return routemap


def generate_random_route(graph, c=0.2):
    """
    Function to generate a random route. Used in random algorithm and genetic algorithm

    Arguments:
    - c: chance of breaking the algorithm. Adds randomness, because the algorithm has a chance of terminating before MAX_TIME is reached
    """
    # Create a route object for every iteration
    route = Route(graph.MAX_TIME)

    # Initiate stations with start distance 0
    candidates = [(station, station, 0) for station in graph.stations.values()]

    while candidates:

        # Pick random station from candidates
        origin_station, new_station, distance = random.choice(candidates)

        # Retrieve connection object and add to route
        if distance != 0:
            new_connection = graph.fetch_connection(origin_station, new_station)
            route.add_connection(new_connection)

        # Add station to route
        route.add_station(origin_station, new_station)

        # Create a list of new candidates
        candidates = route.get_new_options()

        # Random element to determine if another station is added or not
        if len(route.stations) > 1 and random.random() < c:
            break

    return route
