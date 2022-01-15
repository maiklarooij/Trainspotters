# -----------------------------------------------------------
# environment.py
#
# contains functions and constants that represent facts
# these facts never change
# stations, connections, constraints
#
# authors: Mijntje Meijer, Sam Bijhouwer and Maik Larooij
# -----------------------------------------------------------

import csv
import networkx as nx

def get_constants(scale):
    """ Function to retrieve contant variables according to scale """
    
    if scale == 'Holland':
        MAX_ROUTE_TIME = 120
        MAX_ROUTES = 7
        TOTAL_CONNECTIONS = len(load_data(scale = 'Holland')['connections'])
        TOTAL_STATIONS = len(load_data(scale = 'Holland')['stations'])
    else:
        MAX_ROUTE_TIME = 180
        MAX_ROUTES = 20
        TOTAL_CONNECTIONS = len(load_data(scale = 'Nationaal')['connections'])
        TOTAL_STATIONS = len(load_data(scale = 'Nationaal')['stations'])

    return MAX_ROUTE_TIME, MAX_ROUTES, TOTAL_CONNECTIONS, TOTAL_STATIONS

def get_stations(scale):
    """ 
    Retrieves the stations in the format
    Station name: coordinates, connections
    Stores information in a dict
    """

    # Load data
    stations_data = load_data(scale)['stations']
    connections_data = load_data(scale)['connections']

    # We use networkx to create a graph for easily accesing neighbors
    connections_edgelist = [(conn[0], conn[1], float(conn[2])) for conn in connections_data]
    connections_graph = nx.Graph()
    connections_graph.add_weighted_edges_from(connections_edgelist)

    stations_dict = {}

    # For every station, create a dict containing the name, coordinates and connections
    for station in stations_data:

        station_name = station[0]
        station_coor = (station[1], station[2])
        station_connections = [(station[0], station[1], station[2]['weight']) for station in connections_graph.edges(station_name, data=True)]
        station_neighbors = [station for station in connections_graph.neighbors(station_name)]
        
        stations_dict[station_name] = {'coor': station_coor, 'connections': station_connections, 'neighbors': station_neighbors}
    
    return stations_dict


def load_data(scale):
    """ 
    Load in the necessary .csv files. Options: 
    scale = 'Holland' or 'Nationaal'
    """

    with open(f"data/Connecties{scale}.csv", mode="r") as file:
        connections_csv = list(csv.reader(file))[1:]
    
    with open(f"data/Stations{scale}.csv", mode="r") as file:
        stations_csv = list(csv.reader(file))[1:]

    return {'connections': connections_csv, 'stations': stations_csv}

