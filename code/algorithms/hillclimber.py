# -----------------------------------------------------------
# hillclimber.py
#
# Functions to create a hillclimbing algorithm
#
# Authors: Sam Bijhouwer and Maik Larooij
# -----------------------------------------------------------

from code.classes.route import Route
from code.classes.routemap import Routemap
from code.algorithms.randomise import generate_random_route, random_solution
from .constants import get_constants
def generate_routemap(routes):
    """Generates a routemap from a list of route objects"""
    routemap = Routemap()
    for route in routes:
        routemap.add_route(route)

    return routemap

def find_replacement(routemap, index, graph, MAX_TIME, r=1000):
    """
    Generates an X amount of random routes and checks whether replacing the route
    on the given index results in a higher score
    """
    # Store initial score and route
    initial_score = routemap.calc_score(len(graph.connections))
    best_route = routemap.routes[index]

    # Generate an r amount of random routes
    for _ in range(r):
        routemap_copy = routemap.copy()
        random_route = generate_random_route(graph, MAX_TIME)

        # Replace route and check for improvement
        routemap_copy.replace_route(random_route, index)
        new_score = routemap_copy.calc_score(len(graph.connections))

        # Store new best route and score if improved
        if new_score > initial_score:
            initial_score = new_score
            best_route = random_route

    return best_route
    


def hillclimber_solution(graph, start_state=None, restarts=10):
    """
    Generates a solution with hillclimbing algorithm. Takes in a graph and optionally a start state
    Goes over every route in solution and tries random routes and checks for improvement
    Picks route which results in highest improvement of score
    """
    MAX_TIME, MAX_ROUTES = get_constants(graph.scale)

    # Check whether to generate random solution or take given routes
    if start_state == None:
        routemap = random_solution(graph)
    else:
        routemap = generate_routemap(start_state)

    # Run amount of restarts on all routes in routemap
    for _ in range(restarts):
        for index in range(len(routemap.routes)):
            route = find_replacement(routemap, index, graph, MAX_TIME)
            routemap.replace_route(route, index)
    
    return routemap
