import sys

import agents
import environment
import model

scale = sys.argv[1]
algorithm = sys.argv[2]

MAX_ROUTE_TIME, MAX_ROUTES, TOTAL_CONNECTIONS, TOTAL_STATIONS = environment.get_constants(scale)

if algorithm == 'random':
    routemap = agents.random_algorithm(MAX_ROUTE_TIME, MAX_ROUTES, TOTAL_CONNECTIONS, scale)

routemap.print_solution()
routemap.generate_output()