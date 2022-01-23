# -----------------------------------------------------------
# randomise.py
#
# Functions to create a random baseline 
#
# Authors: Sam Bijhouwer and Maik Larooij
# -----------------------------------------------------------

import random

from code.classes.route import Route
from code.classes.routemap import Routemap
from .constants import get_constants

def random_solution(graph):
    """
    Generates a solution on a random basis. Takes in a graph and outputs a routemap object
    """
    MAX_TIME, MAX_ROUTES = get_constants(graph.scale)

    # Randomly pick a number of routes
    number_of_routes = random.randint(1, MAX_ROUTES)

    # Create a routemap object to fill with routes
    routemap = Routemap()

    for _ in range(number_of_routes):

        # Create a route object for every iteration
        route = Route(MAX_TIME)

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

        routemap.add_route(route)
                                                           
    return routemap
