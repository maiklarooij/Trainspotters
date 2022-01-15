from cgi import test
from code.classes.graph import Graph
from code.algorithms.randomise import random_solution

if __name__ == "__main__":

    test_graph = Graph("data/StationsHolland.csv", "data/ConnectiesHolland.csv")
    #print(test_graph.stations)
    #print(test_graph.connections)
    #print(test_graph.stations['Alkmaar'].neighbors)

    random_solution = random_solution(test_graph, 'Holland')
    print(random_solution.calc_score(len(test_graph.connections)))
    random_solution.generate_output(len(test_graph.connections))