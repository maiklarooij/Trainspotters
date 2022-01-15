class Routemap():
    def __init__(self):
        self.routes = []

    def add_route(self, route):
        """ 
        Adds a route object to the routemap
        """
        self.routes.append(route)

    def show_routemap(self):
        """ 
        Prints out the routemap
        """
        for i, route in enumerate(self.routes):
            print(f"Route {i}: {route}. Total time: {route.total_time}")

    def get_total_connections(self):
        all_connections = set()
        for route in self.routes:
            for connection in route.connections:
                all_connections.add(connection)

        return len(all_connections)

    def calc_score(self, graph_connections):
        """ 
        Calculates the score of the routemap according to the formula:
        K = P*10000 - (T*100 + M)
        
        P = Fractions of all connections included in routemap
        T = Number of routes used in routemap
        M = Total time of all routes in minutes
        """

        # Calculate total time of all routes
        M = sum([route.total_time for route in self.routes])

        # Calculate number of stations and number of routes - TODO: maybe make this easier?
        P = self.get_total_connections() / graph_connections
        T = len(self.routes)

        # Calculate final score
        score = (P * 10000) - (T * 100 + M)

        return score