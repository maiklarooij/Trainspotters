# -----------------------------------------------------------
# scores.py
#
# Contains functions for plotting some basic statistics
# like score distributions and minutes vs. fraction of connections plots
# The functions have been used for milestones and results.
#
# Authors: Sam Bijhouwer and Maik Larooij
# -----------------------------------------------------------

import csv
import matplotlib.pyplot as plt
import numpy as np
from codes.algorithms.genetic import GeneticAlgorithm
import pandas as pd
from tabulate import tabulate


# ---------------------------------------------- Milestone: Baseline --------------------------------------------------------------#


def plot_score_distribution(algorithm, graph, test_runs, name):
    """
    Plots a histogram showing the distribution of scores based on a number of test runs.

    Plot found in results/random/experiment/random_score_distribution_holland.png and results/random/random_score_distribution_nationaal.png
    """
    plt.figure()
    scores = np.zeros(test_runs)

    for i in range(test_runs):
        solution = algorithm(graph)
        scores[i] = solution.calc_score(graph.total_connections)

    plt.hist(scores, bins=20)
    plt.title(f"Distribution of scores (algorithm = {name}, n = {test_runs}, scale = {graph.scale})")
    plt.xlabel("Score")
    plt.show()


def plot_minutes_fraction(algorithm, graph, test_runs, name):
    """
    Makes a scatterplot showing the tradeoff between minutes and fraction of connections.

    Plot found in results/random/experiment/fractions_minutes.png
    """
    plt.figure()

    data = {}

    for _ in range(test_runs):
        solution = algorithm(graph)
        score = solution.calc_score(len(graph.connections))
        data[solution.M] = solution.P

    plt.scatter(data.values(), data.keys(), s=10)
    plt.title(f"Fractions vs. minutes (algorithm = {name}, n = {test_runs}, scale = {graph.scale})")
    plt.xlabel("Fraction of total connections in routemap (P)")
    plt.ylabel("Minutes (M)")
    plt.show()


# ---------------------------------------------- Milestone: First algorithm --------------------------------------------------------------#


def plot_beam_score(algorithm, graph, name):
    """
    Plots BF-algorithm score against a range of beam values.

    Plot found in results/bf/experiment/beam_plot.png
    """
    scores = {}
    for beam in range(2, 102, 2):
        solution = algorithm(graph, beam=beam)
        scores[beam] = solution.calc_score(graph.total_connections)

    for beam, score in scores.items():
        print(f"Beam: {beam}, score: {score}")

    plt.plot(scores.keys(), scores.values())
    plt.title(f"Score for different beam values (algorithm = {name}, scale = {graph.scale})")
    plt.xlabel("Beam value")
    plt.ylabel("Routemap score")
    plt.show()


# ---------------------------------------------- Milestone: Second algorithm --------------------------------------------------------------#


def compare_selection(graph):
    """
    Function to compare the different selection methods for a genetic algorithm.

    Plot found in results/genetic/experiment/selection.png
    """
    selections = ["elitism", "tournament", "rws"]

    for selection in selections:
        best_result = [0]
        for i in range(5):
            print(f"{selection}-{i}")
            test = GeneticAlgorithm(graph, 200, 10000, 10000, 0.3, False, selection, "1point").run(graph)

            if test[-1] > best_result[-1]:
                best_result = test

        plt.plot(range(len(best_result)), best_result, label=selection)

    plt.legend()
    plt.title(f"Scores for different selection strategies. n = 5, scale = Nationaal)")
    plt.xlabel("# Generation")
    plt.ylabel("Score")
    plt.show()


def compare_breeding(graph):
    """
    Function to compare the different breeding methods for a genetic algorithm.

    Plot found in results/genetic/experiment/breeding.png
    """
    breedings = ["1point", "2point", "uniform"]

    for breeding in breedings:
        best_result = [0]
        for i in range(5):
            print(f"{breeding}-{i}")
            test = GeneticAlgorithm(graph, 200, 10000, 10000, 0.3, False, "elitism", breeding).run(graph)

            if test[-1] > best_result[-1]:
                best_result = test

        plt.plot(range(len(best_result)), best_result, label=breeding)

    plt.legend()
    plt.title(f"Scores for different breeding strategies (n = 5, scale = Nationaal)")
    plt.xlabel("# Generation")
    plt.ylabel("Score")
    plt.show()


def plot_mutation(csv_file):
    """
    Function to compare the different mutation rates for a genetic algorithm.

    Plot found in results/genetic/experiment/mutation_rate.png
    """
    with open(csv_file, "r") as csv_file:
        reader = csv.DictReader(csv_file)

        mr = []
        scores = []
        for line in reader:
            mr.append(float(line["mutation_rate"]))
            scores.append(float(line["score"]))

    plt.plot(mr, scores)
    plt.title(f"Scores for different mutation rates (n = 5, scale = Nationaal)")
    plt.xlabel("Mutation rate")
    plt.ylabel("Score")
    plt.show()


# ---------------------------------------------- Milestone: Experiment --------------------------------------------------------------#


def plot_breeding_distri(csv_file):
    """
    Function to compare different breeding strategies.

    Plot found in results/genetic/experiment/breeding_distri.png
    """
    df = pd.read_csv(csv_file)

    for breeding in ["1point", "2point"]:

        df_breeding_scores = df[df["breeding"] == breeding]["breeding"]

        plt.hist(df_breeding_scores, bins=20, label=breeding)

    plt.legend()
    plt.title("Distribution of scores for different breeding strategies")
    plt.xlabel("Score")
    plt.show()


def plot_selection_distri(csv_file):
    """
    Function to compare different breeding strategies.

    Plot found in results/genetic/experiment/selection_distri.png
    """
    df = pd.read_csv(csv_file)

    for selection in ["roulette", "tournament", "elitism"]:

        df_selection_scores = df[df["selection"] == selection]["selection"]

        plt.hist(df_selection_scores, bins=20, label=selection)

    plt.legend()
    plt.title("Distribution of scores for different selection strategies")
    plt.xlabel("Score")
    plt.show()


def plot_genhill(genetic_algorithm):
    """
    Plots a score for every generation for a genetic algorithm with hillclimber.
    Needs a

    Plot found in results/genetic/experiment/genetichillclimber.png
    """
    scores = genetic_algorithm.generation_scores
    plt.plot(range(1, len(scores) + 1), scores)
    plt.title(f"Best score after each generation, genetic+hillclimb algorithm")
    plt.xlabel("Generation")
    plt.ylabel("Score")
    plt.show()


def table_hillclimber(csv_file):
    """
    Outputs a markdown table of hillclimber results.

    Tables found in milestones/experiment.md
    Input files: results/genetic/experiment/experiment_hillclimber.csv and results/genetic/experiment/experiment_hillclimber_2.csv
    """
    df = pd.read_csv(csv_file)

    return tabulate(df.groupby["restarts", "r-value"].agg(["mean", "median", "max", "min"]), headers="keys", tablefmt="pipe")


def table_genetic(csv_file):
    """
    Outputs a markdown table of genetic algorithm results.
    This table is huge, thus we return the top 5 best results.

    Tables found in milestones/experiment.md
    Input files: results/genetic/experiment/experiment_genetic.csv and results/genetic/experiment/experiment_genetic_2.csv
    """
    df = pd.read_csv(csv_file)

    return tabulate(
        df.groupby(["breeding", "selection", "generations", "mutate_rate", "gp_size"])
        .agg(["mean", "min", "max", "median"])
        .sort_values([("score", "max")], ascending=False)
        .nlargest(5, ("score", "max")),
        headers="keys",
        tablefmt="pipe",
    )
