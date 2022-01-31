# -----------------------------------------------------------
# visualise.py
#
# Contains a class object to create a train map with folium.
#
# Authors: Sam Bijhouwer and Maik Larooij
# -----------------------------------------------------------

import folium
import random


class TrainMap:
    """ 
    Represents a trainmap, a visualisation made of a routemap (solution).

    Arguments:
    - routemap: the solution routemap
    - graph: the input of the solution, a graph object
    - algorithm: the algorithm used for the solution
    - middle_loc: the location of the middle of the map, standard is the Netherlands
    """

    def __init__(self, routemap, graph, algorithm, middle_loc=[52.37888718, 4.900277615]):
        self.base_map = folium.Map(location=middle_loc, tiles="cartodbpositron", zoom_start=8)
        self.routemap = routemap
        self.graph = graph
        self.algorithm = algorithm

    def station_in_routemap(self, station):
        """
        Returns true if station is in solution, else false.
        """
        return station in [station for route in self.routemap.routes for station in route.stations]

    def add_stations(self):
        """
        Adds markers for every station in routemap.
        Marker is blue for stations present in routemap and red for station not present in routemap.
        """
        stations_in_route = []

        for station in self.graph.stations.values():
            if self.station_in_routemap(station):
                color = "darkblue"
            else:
                color = "red"

            folium.Marker(
                location=[station.coord[0], station.coord[1]],
                popup=f"Station {station.name}. Location: ({station.coord[0]}, {station.coord[1]})",
                icon=folium.Icon(color=color, icon="train", icon_color="#FEBE00", prefix="fa"),
            ).add_to(self.base_map)
            stations_in_route.append(station)

    def add_connections(self):
        """
        Adds lines for every connection in routemap.
        Gives each route a different color.
        """

        # Create random colors for each route
        colors = ["#" + "".join([random.choice("ABCDEF0123456789") for i in range(6)]) for i in range(len(self.routemap.routes))]
        seen_connections = set()

        for i, route in enumerate(self.routemap.routes):
            color = colors[i]
            for connection in route.connections:

                station1_loc = (connection.station1.coord[0], connection.station1.coord[1])
                station2_loc = (connection.station2.coord[0], connection.station2.coord[1])

                # If the connections is in an other route, change the position slightly
                if connection in seen_connections:
                    x = random.uniform(0.002, 0.003)
                    station1_loc = (connection.station1.coord[0] + x, connection.station1.coord[1])
                    station2_loc = (connection.station2.coord[0] + x, connection.station2.coord[1])

                # Create a connection in the visualisation
                folium.PolyLine(
                    locations=[station1_loc, station2_loc],
                    color=color,
                    popup=f"{connection.station1.name} to {connection.station2.name}: {connection.distance} minutes. Route {i+1}",
                ).add_to(self.base_map)

                seen_connections.add(connection)

    def export(self):
        """
        Creates the train map and exports it to an interactive html page.
        """
        self.add_stations()

        self.add_connections()

        self.base_map.save(f"results/{self.algorithm}_solution.html")
