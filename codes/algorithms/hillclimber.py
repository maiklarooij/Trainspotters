# -----------------------------------------------------------
# hillclimber.py
#
# Class definition a Hillclimbing algorithm
#
# Authors: Sam Bijhouwer and Maik Larooij
# -----------------------------------------------------------

from codes.algorithms.randomise import generate_random_route, Random
from codes.classes.routemap import Routemap


class Hillclimber:
    """
    Implements a hillclimbing algorithm.

    Arguments:
    - graph: the input graph with all stations and connections
    - restarts: number of times the hillclimber algorithm does a restart
    - r: number of random routes the hillclimber algorithm generates to try as replacement
    - start_state: optional list of route objects to run the hillclimber algorithm on
    """

    def __init__(self, graph, restarts=10, r=100, start_state=None):
        self.graph = graph
        self.routemap = self.generate_start(start_state)
        self.restarts = restarts
        self.r = r

    def generate_start(self, start_state):
        """
        Turns the start_state into a valid routemap to run the algorithm on.
        Returns a random solution if no start_state is provided
        """
        if start_state == None:
            return Random(self.graph).run()

        routemap = Routemap()
        routemap.add_routes(start_state)
        return routemap

    def find_replacement(self, index):
        """
        Generates an X amount of random routes and checks whether replacing the route
        on the given index results in a higher score
        """
        # Store initial score and route
        initial_score = self.routemap.calc_score(self.graph.total_connections)
        best_route = self.routemap.routes[index]
        routemap_copy = self.routemap.copy()

        # Generate an r amount of random routes
        for _ in range(self.r):

            random_route = generate_random_route(self.graph)

            # Replace route and check for improvement
            routemap_copy.replace_route(random_route, index)
            new_score = routemap_copy.calc_score(self.graph.total_connections)

            # Store new best route and score if improved
            if new_score > initial_score:
                initial_score = new_score
                best_route = random_route

        return best_route

    def run(self):
        """
        Runs the hillclimber algorithm
        """
        for _ in range(self.restarts):

            for index in range(len(self.routemap.routes)):
                route = self.find_replacement(index)
                self.routemap.replace_route(route, index)

        return self.routemap
