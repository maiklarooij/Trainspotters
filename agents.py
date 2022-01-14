# -----------------------------------------------------------
# agents.py
#
# contains algorithms
# 
# authors: Mijntje Meijer, Sam Bijhouwer and Maik Larooij
# -----------------------------------------------------------
 
import random

import model
import environment

def random_algorithm(routemap, max_route_time, scale):

    stations = environment.get_stations(scale)

    for route in routemap.routes.values():
        
        first_station = random.choice(list(stations.keys()))
        candidates = [model.Connection(connection[0], connection[1], connection[2]) for connection in stations[first_station]['connections']]
        route.stationlist.append(first_station)
        total_route_time = 0

        while candidates:

            # Add random connection to route
            new_connection = random.choice(candidates)
            route.add_connection(new_connection)
            route.stationlist.append(new_connection.destination)
            total_route_time += new_connection.distance

            # Update candidates
            candidates = [model.Connection(connection[0], connection[1], connection[2]) for connection in stations[new_connection.destination]['connections']
                          if connection[2] + total_route_time < max_route_time
                          and connection[1] not in route.stationlist]
            print(new_connection.origin, new_connection.destination)
    
    return routemap