from code.classes.route import Route
from code.classes.routemap import Routemap
from .constants import get_constants

import copy

def get_next_station(stations):
    """ 
    Returns the next station with the most connections as starting point of a new route
    """
    stations.sort(key=lambda station: len(station.neighbors), reverse = False)

    return stations.pop()
    
def find_best_station(route, old_routemap, graph):
    """
    Tries to find the best next station based on the score the new routemap achieves when added
    """
    candidates = route.get_new_options()

    scored_candidates = []

    for origin, neighbor, distance in candidates:

        # Create a copy of the route and routemap
        new_route = copy.deepcopy(route)
        new_routemap = copy.deepcopy(old_routemap)
        
        # Add this candidate to the route
        new_route.add_connection(graph.fetch_connection(origin, neighbor))

        # Add route to routemap and calculate score
        new_routemap.add_route(new_route)
        score = new_routemap.calc_score(len(graph.connections))

        scored_candidates.append((origin, neighbor, score))

    # Return the sorted list of candidates based on the score
    return sorted(scored_candidates, key=lambda x: x[2], reverse=True)

def greedy_solution(graph, scale):
    """
    Generates a solution on a greedy basis. Takes in a graph and outputs a routemap object
    Starts with the station with the most connections,
    adds stations based on their resulting routemap score
    """

    MAX_TIME, MAX_ROUTES = get_constants(scale)

    # Create a routemap object to fill with routes
    routemap = Routemap()

    stations_visited = set()
    stations = list(graph.stations.values())

    # Go on until all stations are reached or MAX_ROUTES are used
    while (len(stations_visited) != len(graph.stations)) and len(routemap.routes) != MAX_ROUTES:

        route = Route(MAX_TIME)

        # Get station with least connections as start station
        start_station = get_next_station(stations)
        route.add_station(start_station, start_station)

        # While there are options possible
        while route.get_new_options():
            
            # Choose best station
            origin_station, new_station, score = find_best_station(route, routemap, graph)[0]
            new_connection = graph.fetch_connection(origin_station, new_station)

            # Add to route
            route.add_connection(new_connection)
            route.add_station(origin_station, new_station)

        routemap.add_route(route)

        # Add stations from newly added route to visited stations
        for station in route.stations:
            stations_visited.add(station)

    return routemap