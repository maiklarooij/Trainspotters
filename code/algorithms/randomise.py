# -----------------------------------------------------------
# randomise.py
#
# Functions to create a random baseline 
#
# Authors: Mijntje Meijer, Sam Bijhouwer and Maik Larooij
# -----------------------------------------------------------

import random

from code.classes.route import Route
from code.classes.routemap import Routemap

def get_constants(scale):
    """ 
    Determine constants based on the scale
    """ 
    if scale == 'Holland':
        MAX_TIME = 120
        MAX_ROUTES = 7
    else: 
        MAX_TIME = 180
        MAX_ROUTES = 20
    
    return MAX_TIME, MAX_ROUTES

def random_solution(graph, scale):
    """
    Generates a solution on a random basis. Takes in a graph and outputs a routemap object
    """
    MAX_TIME, MAX_ROUTES = get_constants(scale)

    # Randomly pick a number of routes
    number_of_routes = random.randint(1, MAX_ROUTES)

    # Create a routemap object to fill with routes
    routemap = Routemap()

    for _ in range(number_of_routes):

        # Create a route object for every iteration
        route = Route()

        # Initiate stations with start distance 0
        candidates = [(station, 0) for station in graph.stations.values()]

        while candidates:

            # Pick random station from candidates
            new_station = random.choice(candidates)

            # If not first station (i.e. distance is not 0), add connection between stations to the route
            if new_station[1] != 0:
                new_connection = graph.fetch_connection(new_station[0], origin_station[0])
                route.add_connection(new_connection)

            route.add_station(new_station[0], new_station[1])

            # Generate new candidates, must not exceed total time and neighbor must not already be in solution
            candidates = [(neighbor, distance) for neighbor, distance in new_station[0].neighbors.items() if route.total_time + distance < MAX_TIME 
                                                                                                        and neighbor not in route.stations]

            # Remember origin station for next iteration
            origin_station = new_station

        routemap.add_route(route)
                                                                                        
    return routemap
