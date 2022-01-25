import sys
import argparse
from code.algorithms.hillclimber import hillclimber_solution

from code.classes.graph import Graph
from code.algorithms.randomise import random_solution
from code.algorithms.greedy import greedy_solution
from code.algorithms.breadthfirst import breadth_first_solution
from code.algorithms.hillclimber import hillclimber_solution
from code.algorithms.genetic import GeneticAlgorithm
from code.visualisation.visualise import make_train_map
from code.visualisation.scores import plot_score_distribution, plot_minutes_fraction

if __name__ == "__main__":

    # Command line arguments
    p = argparse.ArgumentParser()
    p.add_argument('-s', '--scale', help='Scale to run algorithms on. Options = "Holland" or "Nationaal"', default='Holland',
                   type=str)
    p.add_argument('-a', '--algorithm', help='Algorithm to run. Options = "random", "greedy", "bf", "hillclimber", "genetic".', default='random', type=str)
    p.add_argument('-gs', '--genes_size', help='Number of random genes (=routes) to generate for GA', default=1000, type=int)
    p.add_argument('-ps', '--pop_size', help='Number of random combinations of genes (=routemaps) to generate for GA', default=1000, type=int)
    p.add_argument('-mr', '--mutation_rate', help='Chance of mutations', default=0.2, type=float)
    args = p.parse_args(sys.argv[1:])

    # Scale = 'Nationaal' or 'Holland'
    # Algorithm = 'random', 'greedy', 'bf', 'genetic'
    scale = args.scale
    algorithm = args.algorithm
    
    # Make test graph based on scale
    test_graph = Graph(f"data/Stations{scale}.csv", f"data/Connecties{scale}.csv", scale)
    nr_connections = len(test_graph.connections)
    algorithms = {'random': random_solution, 'greedy': greedy_solution, 'bf': breadth_first_solution, 
                  'genetic': GeneticAlgorithm(test_graph, 100, args.genes_size, args.pop_size, args.mutation_rate).run,
                  'hillclimber': hillclimber_solution}

    # Run algorithm
    solution = algorithms[algorithm](test_graph)

    # Generate results
    solution.generate_output(nr_connections)
    make_train_map(solution, test_graph, [52.37888718, 4.900277615], algorithm)