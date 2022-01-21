# -----------------------------------------------------------
# breadthfirst.py
#
# Functions to implement a breadth first search algorithm
#
# Authors: Mijntje Meijer, Sam Bijhouwer and Maik Larooij
# -----------------------------------------------------------

from code.classes.route import Route
from code.classes.routemap import Routemap
from .constants import get_constants

import copy

def measure_increase(route, routemap, candidate, graph):
    """
    Takes in a route, routemap and candidate.
    Measures the increase if the candidate would be added to the graph.
    """
    # Make copies
    routemap_copy = copy.deepcopy(routemap)
    route_copy = copy.deepcopy(route)

    # Add candidate station to route
    route_copy.add_station(candidate[0], candidate[1])
    route_copy.add_connection(graph.fetch_connection(candidate[0], candidate[1]))

    # Add modified route to routemap
    routemap_copy.add_route(route_copy)

    # Measure increase
    increase = routemap_copy.calc_score(len(graph.connections)) - routemap.calc_score(len(graph.connections))

    return route_copy, increase

def breadth_first_solution(graph, scale, beam=5):
    """
    Implements a breadth first search algorithm.
    Uses beam search to prune the options.
    """
    MAX_TIME, MAX_ROUTES = get_constants(scale)

    routemap = Routemap()

    while len(routemap.routes) != MAX_ROUTES:

        # At the start of a route, initialize routes with all different stations as start states
        children = [Route(MAX_TIME, start_station=station) for station in graph.stations.values()]
        best_option = (None, 0)

        # While there are options available resulting in a higher score
        while children:

            # Keep track of routes that are scored
            scored_routes = []

            # Go through all options
            for route in children:

                # Get possible candidates for this option
                candidates = route.get_new_options()

                # For every candidate, measure the increase if this candidate would be added
                for candidate in candidates:

                    route_copy, increase = measure_increase(route, routemap, candidate, graph)

                    # Keep route in memory if it is an improvement
                    if increase > 0:
                        scored_routes.append((route_copy, increase))
                    
                    # If route is the best route that was found until now, save it!
                    if increase > best_option[1]:
                        best_option = (route_copy, increase)

            # Create new options, keep only the x (beam value) highest increasing routes
            children = [route[0] for route in sorted(scored_routes, key=lambda x: x[1], reverse = True)[:beam]]

        # If there is no option resulting in a higher score, stop the algorithm
        if not best_option[0]:
            break
        
        # Add route
        routemap.add_route(best_option[0])

    return routemap 
