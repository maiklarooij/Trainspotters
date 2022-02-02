# -----------------------------------------------------------
# breadthfirst.py
#
# Class definition of a breadth-first search algorithm
# Contains pruning based on beam search
#
# Authors: Sam Bijhouwer and Maik Larooij
# -----------------------------------------------------------

from src.classes.route import Route
from src.classes.routemap import Routemap


class BreadthFirst:
    """
    Implements a breadth-first algorithm.

    Arguments:
    - graph: the input graph with all stations and connections
    - beam: integer to prune the options for each step
    """

    def __init__(self, graph, beam=14):
        self.graph = graph
        self.beam = beam
        self.routemap = Routemap()

    def measure_increase(self, route, candidate):
        """
        Takes in a route, routemap and candidate.
        Measures the increase if the candidate would be added to the graph.
        """

        # Make copies
        routemap_copy = self.routemap.copy()
        route_copy = route.copy()

        # Add candidate station to route
        route_copy.add_station(candidate[0], candidate[1])
        route_copy.add_connection(self.graph.fetch_connection(candidate[0], candidate[1]))

        # Add modified route to routemap
        routemap_copy.add_route(route_copy)

        # Measure increase
        increase = routemap_copy.calc_score(self.graph.total_connections) - self.routemap.calc_score(self.graph.total_connections)

        return route_copy, increase

    def run(self):
        """
        Runs the breadth-first algorithm
        """
        while len(self.routemap.routes) != self.graph.MAX_ROUTES:

            # At the start of a route, initialize routes with all different stations as start states
            children = [Route(self.graph.MAX_TIME, start_station=station) for station in self.graph.stations.values()]
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

                        route_copy, increase = self.measure_increase(route, candidate)

                        # Keep route in memory if it is an improvement
                        if increase > 0:
                            scored_routes.append((route_copy, increase))

                        # If route is the best route that was found until now, save it!
                        if increase > best_option[1]:
                            best_option = (route_copy, increase)

                # Create new options, keep only the x (beam value) highest increasing routes
                children = [route[0] for route in sorted(scored_routes, key=lambda x: x[1], reverse=True)[: self.beam]]

            # If there is no option resulting in a higher score, stop the algorithm
            if not best_option[0]:
                break

            # Add route
            self.routemap.add_route(best_option[0])

        return self.routemap
