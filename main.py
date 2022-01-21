import sys
import numpy as np
import matplotlib.pyplot as plt

from code.classes.graph import Graph
from code.algorithms.randomise import random_solution
from code.algorithms.greedy import greedy_solution
from code.algorithms.breadthfirst import breadth_first_solution
from code.visualisation.visualise import make_train_map
from code.visualisation.scores import plot_score_distribution, plot_minutes_fraction

if __name__ == "__main__":

    # Scale = 'Nationaal' or 'Holland'
    scale = sys.argv[1]

    # ------------------------------------------- Random ------------------------------------------- #

    test_graph = Graph(f"data/Stations{scale}.csv", f"data/Connecties{scale}.csv")

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
    test = breadth_first_solution(test_graph, scale, 3)
    test.generate_output(len(test_graph.connections))

    make_train_map(test, test_graph, [52.37888718, 4.900277615], 'breadth_first')
