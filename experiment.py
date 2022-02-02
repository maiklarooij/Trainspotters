# -----------------------------------------------------------
# experiment.py
#
# Script to run experiment, comparing different algorithms and parameters.
#
# Authors: Sam Bijhouwer and Maik Larooij
# -----------------------------------------------------------

import argparse
import csv
import sys
import time

from src.algorithms.breadthfirst import BreadthFirst
from src.algorithms.genetic import GeneticAlgorithm
from src.algorithms.hillclimber import Hillclimber
from src.algorithms.randomise import Random
from src.classes.graph import Graph


def experiment_random(graph, runs=100000):
    """
    Executes random algorithm a number of times and writes results to a csv file named experiment_random.csv
    """
    with open("results/random/experiment/experiment_random.csv", "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["run", "score"])

        for i in range(runs):
            rs = Random(graph).run()
            score = rs.calc_score(graph.total_connections)

            writer.writerow([i + 1, score])


def experiment_bf(graph):
    """
    Executes breadth first algorithm for beam values between 2 and 100 and writes results to a csv file named experiment_bf.csv
    """
    with open("results/bf/experiment/experiment_bf.csv", "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["beam", "score"])

        for beam in range(2, 102, 2):
            bf = BreadthFirst(graph, beam=beam).run()
            score = bf.calc_score(graph.total_connections)

            writer.writerow([beam, score])


def experiment_hillclimber(graph):
    """
    Executes hillclimber algorithm for different values for restart and r and writes results to a csv file named experiment_hillclimber.csv
    """
    restarts = [1, 5, 10, 20]
    r_values = [100, 500, 1000]

    with open("results/hillclimber/experiment/experiment_hillclimber.csv", "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["run", "restarts", "r-value", "score"])

        option = 1
        for restart in restarts:
            for r_value in r_values:

                print(f"option {option} of 2")
                print(f"{restart}:{r_value}")
                start = time.time()
                run = 1
                while time.time() - start < 300:
                    hc = Hillclimber(graph, restarts=restart, r=r_value).run()
                    score = hc.calc_score(graph.total_connections)

                    writer.writerow([run, restart, r_value, score])
                    run += 1
                option += 1


def experiment_genetic(graph):
    """
    Executes genetic algorithm for different configurations and writes results to a csv file named experiment_genetic.csv
    """
    breedings = ["1point", "2point"]
    selections = ["elitism", "tournament", "rws"]
    generations = [50, 100, 200]
    mutate_rates = range(0, 12, 2)
    genes_and_pop_size = [100, 500, 1000]

    with open("results/genetic/experiment/experiment_genetic.csv", "w", newline="") as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(["run", "breeding", "selection", "generations", "mutate_rate", "gp_size", "score"])

        option = 1

        # Go through all options
        for breeding in breedings:
            for selection in selections:
                for generation in generations:
                    for mutate_rate in mutate_rates:
                        for gp_size in genes_and_pop_size:

                            print(f"option {option} of 324")
                            print(f"{breeding}:{selection}:{generation}:{mutate_rate}:{gp_size}")

                            # Give each option a minute to run as often as possible.
                            start = time.time()
                            run = 1
                            while time.time() - start < 60:
                                ga = GeneticAlgorithm(graph, generation, gp_size, gp_size, mutate_rate / 10, False, selection, breeding).run(graph)
                                score = ga.calc_score(graph.total_connections)
                                writer.writerow([run, breeding, selection, generation, mutate_rate / 10, gp_size, score])
                                run += 1

                            option += 1


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('scale', help='Scale to run experiment on. Options = "Holland" or "Nationaal"', default="Holland", type=str)
    p.add_argument('algorithm', help="Algorithm to run experiment on", default='all', type=str)
    args = p.parse_args(sys.argv[1:])

    experiment_graph = Graph(f"data/Stations{args.scale}.csv", f"data/Connecties{args.scale}.csv", args.scale)
    experiments = {"random": experiment_random, "genetic": experiment_genetic, "bf": experiment_bf, "hillclimber": experiment_hillclimber}

    if args.algorithm == 'all':
        for function in experiments.values():
            function(experiment_graph)
    else:
        experiments[args.algorithm](experiment_graph)
