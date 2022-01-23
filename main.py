import sys
import argparse

from code.classes.graph import Graph
from code.algorithms.randomise import random_solution
from code.algorithms.greedy import greedy_solution
from code.algorithms.breadthfirst import breadth_first_solution
from code.visualisation.visualise import make_train_map
from code.visualisation.scores import plot_score_distribution, plot_minutes_fraction

if __name__ == "__main__":

    # Command line arguments
    p = argparse.ArgumentParser()
    p.add_argument('-s', '--scale', help='Scale to run algorithms on. Options = "Holland" or "Nationaal"', default='Holland',
                   type=str)
    p.add_argument('-a', '--algorithm', help='Algorithm to run. Options = "random", "greedy", "bf".', default='random', type=str)
    args = p.parse_args(sys.argv[1:])

    # Scale = 'Nationaal' or 'Holland'
    # Algorithm = 'random', 'greedy', 'bf'
    scale = args.scale
    algorithm = args.algorithm
    
    # Make test graph based on scale
    test_graph = Graph(f"data/Stations{scale}.csv", f"data/Connecties{scale}.csv", scale)
    nr_connections = len(test_graph.connections)
    algorithms = {'random': random_solution, 'greedy': greedy_solution, 'bf': breadth_first_solution}

    # Run algorithm
    solution = algorithms[algorithm](test_graph)

    # Generate results
    solution.generate_output(nr_connections)
    make_train_map(solution, test_graph, [52.37888718, 4.900277615], algorithm)

    # ------------------------------------------- Random ------------------------------------------- #

    # test_graph = Graph(f"data/Stations{scale}.csv", f"data/Connecties{scale}.csv")

    # random_solution = random_solution(test_graph, scale)
    # random_solution.generate_output(len(test_graph.connections))

    # make_train_map(random_solution, test_graph, [52.37888718, 4.900277615], 'random_solution')

    # plot_minutes_fraction(random_solution, test_graph, scale, 10000, 'Random')

    # ------------------------------------------- Greedy ------------------------------------------- #

    # greedy_solution = greedy_solution(test_graph, scale)
    # greedy_solution.generate_output(len(test_graph.connections))

    # make_train_map(greedy_solution, test_graph, [52.37888718, 4.900277615], 'greedy_solution')

    # ---------------------------------------------------------------------------------------------- #

    #for i in [1, 2, 3, 4, 5, 10]:
    # test = breadth_first_solution(test_graph, scale, 3)
    # test.generate_output(len(test_graph.connections))

    # make_train_map(test, test_graph, [52.37888718, 4.900277615], 'breadth_first')
