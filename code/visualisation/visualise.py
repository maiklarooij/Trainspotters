# -----------------------------------------------------------
# visualise.py
#
# Contains a function to create a Folium map of a routemap result
#
# Authors: Sam Bijhouwer and Maik Larooij
# -----------------------------------------------------------

import folium
import random

def make_train_map(routemap, graph, middle_loc, algorithm):
    """ 
    Creates a folium train map, showing stations and connections.
    Takes in the complete graph and the routemap extracted from the graph.
    """

    # Create a basemap with a given middle point
    base_map = folium.Map(location = middle_loc, tiles = 'cartodbpositron', zoom_start = 8)

    stations_in_route = []
    # Add a marker for every station
    for route in routemap.routes:
        for station in route.stations:
            folium.Marker(
                location = [station.coord[0], station.coord[1]],
                popup = f"Station {station.name}. Location: ({station.coord[0]}, {station.coord[1]})",
                icon = folium.Icon(color = 'darkblue', icon = 'train', icon_color = '#FEBE00', prefix = 'fa')).add_to(base_map)
            stations_in_route.append(station)

    # Add stations that are not in route
    for station in graph.stations.values():
        if station not in stations_in_route:
            folium.Marker(
                location = [station.coord[0], station.coord[1]],
                popup = f"Station {station.name}. Location: ({station.coord[0]}, {station.coord[1]})",
                icon = folium.Icon(color = 'red', icon = 'train', icon_color = '#FEBE00', prefix = 'fa')).add_to(base_map)

    # Create random colors for each route
    colors = ["#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)]) for i in range(len(routemap.routes))]
    seen_connections = set()

    for i, route in enumerate(routemap.routes):
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
                locations = [station1_loc, station2_loc],
                color = color,
                popup = f"{connection.station1.name} to {connection.station2.name}: {connection.distance} minutes. Route {i+1}").add_to(base_map)
            
            seen_connections.add(connection)

    base_map.save(f"results/{algorithm}_solution.html")