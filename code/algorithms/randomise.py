import random

from code.classes.route import Route
from code.classes.routemap import Routemap


def random_solution(graph, scale):
    """
    Generates a solution on a random basis. Takes in a graph and outputs a routemap object
    """

    if scale == 'Holland':
        MAX_TIME = 120
        MAX_ROUTES = 7

    # Randomly pick a number of routes
    number_of_routes = random.randint(1, MAX_ROUTES)

    routemap = Routemap()

    for _ in range(number_of_routes):

        route = Route()

        # Initiate stations with start distance 0
        candidates = [(station, station, 0) for station in graph.stations.values()]
        # new_station = random.choice(candidates)
        # route.add_station(0, new_station, 0)

        while candidates:
            # Pick random station from candidates
            new_station = random.choice(candidates)
  
            if new_station[2] != 0:
                new_connection = graph.fetch_connection(new_station[0], new_station[1])
                route.add_connection(new_connection)

            route.add_station(new_station[0], new_station[1], new_station[2])

            
            candidates = [(station, neighbor, distance) for station in [route.stations[0], route.stations[-1]]
                                                        for neighbor, distance in station.neighbors.items()
                                                        if route.total_time + distance < MAX_TIME and
                                                        neighbor not in route.stations]
                        # candidates = [(station.neighbors) for station in [new_station[0], new_station[-1]] if route.total_time + distance < MAX_TIME 
            #                                                                                             and neighbor not in route.stations]
            # If not first station, add connection between stations to the route
            # if new_station[1] != 0:
            #     new_connection = [connection for connection in graph.connections if connection.station1 in (new_station[0], origin_station[0]) and connection.station2 in (new_station[0], origin_station[0])][0]
            #     route.add_connection(new_connection)
            # Generate new candidates, must not exceed total time and neighbor must not already be in solution
            # candidates = [(neighbor, distance) for neighbor, distance in new_station[0].neighbors.items() if route.total_time + distance < MAX_TIME 
            #                                                                                             and neighbor not in route.stations]
            # Remember origin station for next iteration
            # origin_station = new_station

        routemap.add_route(route)
                                                                                        
    return routemap
