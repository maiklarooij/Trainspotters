# -----------------------------------------------------------
# main.py
#
# Used to run algorithms.
#
# Authors: Sam Bijhouwer and Maik Larooij
# -----------------------------------------------------------

import sys
import argparse

from code.algorithms.breadthfirst import breadth_first_solution
from code.algorithms.genetic import GeneticAlgorithm
from code.algorithms.greedy import greedy_solution
from code.algorithms.hillclimber import hillclimber_solution
from code.algorithms.randomise import random_solution
from code.classes.graph import Graph
from code.visualisation.visualise import TrainMap


if __name__ == "__main__":

    # Command line arguments
    p = argparse.ArgumentParser()

    # All algorithms arguments
    p.add_argument("-s", "--scale", help='Scale to run algorithms on. Options = "Holland" or "Nationaal"', default="Holland", type=str)
    p.add_argument("-a", "--algorithm", help='Algorithm to run. Options = "random", "greedy", "bf", "hillclimber", "genetic".',
                   default="random", type=str)

    # Genetic algorithm optional arguments
    p.add_argument("-gs", "--genes_size", help="Number of random genes (=routes) to generate for GA", default=1000, type=int)
    p.add_argument("-ps", "--pop_size", help="Number of random combinations of genes (=routemaps) to generate for GA", default=1000, type=int)
    p.add_argument("-mr", "--mutation_rate", help="Chance of mutations", default=0.2, type=float)
    p.add_argument("-gn", "--generations", help="Number of generations", default=100, type=int)
    p.add_argument("-hc", "--hillclimber", help="Option to use hillclimber in genetic algorithm", default="false", type=str)
    p.add_argument("-sl", "--selection", help='Selection strategies. Options = "rws", "elitism", "tournament"', default="elitism", type=str)
    p.add_argument("-br", "--breeding", help='Breeding strategies. Options = "1point", "2point", "uniform"', default="1point", type=str)
    hillclimber_option = {"true": True, "false": False}

    args = p.parse_args(sys.argv[1:])

    # Scale = 'Nationaal' or 'Holland'
    # Algorithm = 'random', 'greedy', 'bf', 'genetic'
    scale = args.scale
    algorithm = args.algorithm

    # Make test graph based on scale
    test_graph = Graph(f"data/Stations{scale}.csv", f"data/Connecties{scale}.csv", scale)
    nr_connections = test_graph.total_connections
    algorithms = {
        "random": random_solution,
        "greedy": greedy_solution,
        "bf": breadth_first_solution,
        "genetic": GeneticAlgorithm(
            test_graph,
            args.generations,
            args.genes_size,
            args.pop_size,
            args.mutation_rate,
            hillclimber_option[args.hillclimber],
            args.selection,
            args.breeding,
        ).run,
        "hillclimber": hillclimber_solution,
    }

    # Run algorithm
    solution = algorithms[algorithm](test_graph)

    # Generate results
    solution.generate_output(nr_connections)
    TrainMap(solution, test_graph, algorithm).export()
