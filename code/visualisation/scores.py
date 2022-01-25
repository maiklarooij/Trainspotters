# -----------------------------------------------------------
# scores.py
#
# Contains functions for plotting some basic statistics
# like score distributions and minutes vs. fraction of connections plots
#
# Authors: Sam Bijhouwer and Maik Larooij
# -----------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np

def plot_score_distribution(algorithm, graph, scale, test_runs, name):
    """
    Plots a histogram showing the distribution of scores based on a number of test runs
    """
    plt.figure()
    scores = np.zeros(test_runs)

    for i in range(test_runs):
        solution = algorithm(graph)
        scores[i] = solution.calc_score(len(graph.connections))

    plt.hist(scores, bins = 20)
    plt.title(f'Distribution of scores (algorithm = {name}, n = {test_runs}, scale = {scale})')
    plt.xlabel('Score')
    plt.show()

def plot_minutes_fraction(algorithm, graph, scale, test_runs, name):
    """
    Makes a scatterplot showing the tradeoff between minutes and fraction of connections
    """
    plt.figure()

    data = {}

    for _ in range(test_runs):
        solution = algorithm(graph)
        score = solution.calc_score(len(graph.connections))
        data[solution.M] = solution.P

    plt.scatter(data.values(), data.keys(), s = 10)
    plt.title(f'Fractions vs. minutes (algorithm = {name}, n = {test_runs}, scale = {scale})')
    plt.xlabel('Fraction of total connections in routemap (P)')
    plt.ylabel('Minutes (M)')
    plt.show()


def plot_beam_score(algorithm, graph, name):

    scores = {}
    for beam in range(2, 102, 2):
        solution = algorithm(graph, beam=beam)
        scores[beam] = solution.calc_score(len(graph.connections))

    for beam, score in scores.items():
        print(f"Beam: {beam}, score: {score}")

    plt.plot(scores.keys(), scores.values())
    plt.title(f'Score for different beam values (algorithm = {name}, scale = {graph.scale})')
    plt.xlabel('Beam value')
    plt.ylabel('Routemap score')
    plt.show()
