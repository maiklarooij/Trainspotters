import random

from code.classes.route import Route
from code.classes.routemap import Routemap


def random_solution(graph, scale):
    """
    Generates a solution on a random basis
    """

    if scale == 'Holland':
        MAX_TIME = 120
        MAX_ROUTES = 7

    number_of_routes = random.randint(1, MAX_ROUTES)

    routemap = Routemap()

    for i in range(number_of_routes):

        route = Route()

        # Initiate stations with start distance 0
        candidates = [(station, 0) for station in graph.stations.values()]

        while candidates:

            # Pick random station from candidates
            new_station = random.choice(candidates)

            if new_station[1] != 0:
                new_connection = [connection for connection in graph.connections if connection.station1 in (new_station[0], origin_station[0]) and connection.station2 in (new_station[0], origin_station[0])][0]
                route.add_connection(new_connection)

            route.add_station(new_station[0], new_station[1])

            # Generate new candidates, must not exceed total time and neighbor must not already be in solution
            candidates = [(neighbor, distance) for neighbor, distance in new_station[0].neighbors.items() if route.total_time + distance < MAX_TIME 
                                                                                                        and neighbor not in route.stations]

            origin_station = new_station

        routemap.add_route(route)
                                                                                        
    return routemap