import random
import sys

from code.classes.graph import Graph
from code.algorithms.randomise import random_solution
from code.visualisation.visualise import make_train_map

if __name__ == "__main__":

    # Scale = 'Nationaal' or 'Holland'
    scale = sys.argv[1]

    test_graph = Graph(f"data/Stations{scale}.csv", f"data/Connecties{scale}.csv")
    #print(test_graph.stations)
    #print(test_graph.connections)
    #print(test_graph.stations['Alkmaar'].neighbors)

    random_solution = random_solution(test_graph, scale)
    print(random_solution.calc_score(len(test_graph.connections)))
    random_solution.generate_output(len(test_graph.connections))

    make_train_map(random_solution, test_graph, [52.37888718, 4.900277615])
