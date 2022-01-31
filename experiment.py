# -----------------------------------------------------------
# experiment.py
#
# Script to run experiment, comparing different algorithms and parameters.
#
# Authors: Sam Bijhouwer and Maik Larooij
# -----------------------------------------------------------

from argparse import ArgumentParser
import csv
import sys
import time

from code.algorithms.genetic import GeneticAlgorithm
from code.classes.graph import Graph


def experiment(graph):

    breedings = ["1point", "2point"]
    selections = ["elitism", "tournament", "rws"]
    generations = [50, 100, 200]
    mutate_rates = range(0, 12, 2)
    genes_and_pop_size = [100, 500, 1000]

    with open("experiment.csv", "w", newline="") as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(["run", "breeding", "selection", "generations", "mutate_rate", "gp_size", "score"])

        option = 1
        for breeding in breedings:
            for selection in selections:
                for generation in generations:
                    for mutate_rate in mutate_rates:
                        for gp_size in genes_and_pop_size:
                            
                            if option > 44:
                                print(f"option {option} of 405")
                                print(f"{breeding}:{selection}:{generation}:{mutate_rate}:{gp_size}")

                                start = time.time()
                                run = 1
                                while time.time() - start < 60:
                                    ga = GeneticAlgorithm(graph, generation, gp_size, gp_size, mutate_rate / 10, False, selection, breeding).run(graph)
                                    score = ga.calc_score(graph.total_connections)
                                    writer.writerow([run, breeding, selection, generation, mutate_rate / 10, gp_size, score])
                                    run += 1

                            option += 1


if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument("-s", "--scale", help='Scale to run experiment on. Options = "Holland" or "Nationaal"', default="Holland", type=str)
    args = p.parse_args(sys.argv[1:])

    experiment_graph = Graph(f"data/Stations{args.scale}.csv", f"data/Connecties{args.scale}.csv", args.scale)

    experiment(experiment_graph)
