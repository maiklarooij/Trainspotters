# -----------------------------------------------------------
# greedy.py
#
# Class definition a greedy algorithm
#
# Authors: Sam Bijhouwer and Maik Larooij
# -----------------------------------------------------------

from src.classes.route import Route
from src.classes.routemap import Routemap


class Greedy:
    """
    Implements a greedy algorithm.

    Arguments:
    - graph: the input graph with all stations and connections
    """

    def __init__(self, graph):
        self.graph = graph
        self.routemap = Routemap()

    def get_next_station(self, stations):
        """
        Returns the next station with the most connections as starting point of a new route
        """
        stations.sort(key=lambda station: len(station.neighbors), reverse=False)

        return stations.pop()

    def find_best_station(self, route):
        """
        Returns the best next station based on the score the new routemap achieves when added
        """
        candidates = route.get_new_options()
        scored_candidates = []

        for origin, neighbor, _ in candidates:

            # Create a copy of the route and routemap
            new_routemap = self.routemap.copy()
            new_route = route.copy()

            # Add this candidate to the route
            new_route.add_connection(self.graph.fetch_connection(origin, neighbor))

            # Replace route in routemap and calculate score
            new_routemap.add_route(new_route)
            score = new_routemap.calc_score(self.graph.total_connections)

            scored_candidates.append((origin, neighbor, score))

        # Return the sorted list of candidates based on the score
        return sorted(scored_candidates, key=lambda x: (x[2], x[1].name), reverse=True)[0]

    def fill_route(self, route):
        """
        Fills route with connections while there are still new options to add
        """
        while route.get_new_options():
            # Choose best station
            origin_station, new_station, _ = self.find_best_station(route)
            new_connection = self.graph.fetch_connection(origin_station, new_station)

            # Add to route
            route.add_connection(new_connection)
            route.add_station(origin_station, new_station)

        return route

    def run(self):
        """
        Runs the greedy algorithm
        """
        stations_visited = set()
        stations = list(self.graph.stations.values())

        # Go on until all stations are reached or MAX_ROUTES are used
        while len(stations_visited) != len(self.graph.stations) and len(self.routemap.routes) != self.graph.MAX_ROUTES:

            route = Route(self.graph.MAX_TIME)

            # Get station with most connections as start station
            stations = [station for station in stations if station not in stations_visited]
            start_station = self.get_next_station(stations)

            route.add_station(start_station, start_station)

            # Fill route with connections
            route = self.fill_route(route)

            self.routemap.add_route(route)

            # Add stations from newly added route to visited stations
            for station in route.stations:
                stations_visited.add(station)

        return self.routemap
