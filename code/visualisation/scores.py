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
import csv

from code.algorithms.genetic import GeneticAlgorithm

def plot_score_distribution(algorithm, graph, test_runs, name):
    """
    Plots a histogram showing the distribution of scores based on a number of test runs.
    """
    plt.figure()
    scores = np.zeros(test_runs)

    for i in range(test_runs):
        solution = algorithm(graph)
        scores[i] = solution.calc_score(graph.total_connections)

    plt.hist(scores, bins = 20)
    plt.title(f'Distribution of scores (algorithm = {name}, n = {test_runs}, scale = {graph.scale})')
    plt.xlabel('Score')
    plt.show()

def plot_minutes_fraction(algorithm, graph, test_runs, name):
    """
    Makes a scatterplot showing the tradeoff between minutes and fraction of connections.
    """
    plt.figure()

    data = {}

    for _ in range(test_runs):
        solution = algorithm(graph)
        score = solution.calc_score(len(graph.connections))
        data[solution.M] = solution.P

    plt.scatter(data.values(), data.keys(), s = 10)
    plt.title(f'Fractions vs. minutes (algorithm = {name}, n = {test_runs}, scale = {graph.scale})')
    plt.xlabel('Fraction of total connections in routemap (P)')
    plt.ylabel('Minutes (M)')
    plt.show()

def plot_beam_score(algorithm, graph, name):
    """
    Plots BF-algorithm score against a range of beam values.
    """
    scores = {}
    for beam in range(2, 102, 2):
        solution = algorithm(graph, beam=beam)
        scores[beam] = solution.calc_score(graph.total_connections)

    for beam, score in scores.items():
        print(f"Beam: {beam}, score: {score}")

    plt.plot(scores.keys(), scores.values())
    plt.title(f'Score for different beam values (algorithm = {name}, scale = {graph.scale})')
    plt.xlabel('Beam value')
    plt.ylabel('Routemap score')
    plt.show()

def store_genetic_scores(graph):

    mutate_rate = range(2, 6)
    generation_size = [200]

    with open('genetic_scores.csv', 'w', newline='') as wf:

        writer = csv.writer(wf)
        writer.writerow(['generations', 'mutation_rate', 'score'])
        j = 1
        for mr in mutate_rate:
            for gsize in generation_size:

                top_result = 0
                for i in range(5):
                    print(f'option {j}-{i}')
                    result = GeneticAlgorithm(graph, gsize, 10000, 10000, mr /10, False, 'elitism', '1point').run(graph).calc_score(graph.total_connections)
                    if result > top_result:
                        top_result = result
                writer.writerow([gsize, mr/10, top_result])

                j += 1

def compare_selection(graph):

    selections = ['elitism', 'tournament', 'rws']

    for selection in selections:
        best_result = [0]
        for i in range(5):
            print(f"{selection}-{i}")
            test = GeneticAlgorithm(graph, 200, 10000, 10000, 0.3, False, selection, '1point').run(graph)

            if test[-1] > best_result[-1]:
                best_result = test

        plt.plot(range(len(best_result)), best_result, label=selection)
    
    plt.legend()
    plt.title(f'Scores for different selection strategies. n = 5, scale = Nationaal)')
    plt.xlabel('# Generation')
    plt.ylabel('Score')
    plt.show()

def compare_breeding(graph):

    breedings = ['1point', '2point', 'uniform']

    with open('breeding_output.csv', 'w', newline='') as wf:
        writer = csv.writer(wf)

        writer.writerow(['breeding', 'score', 'generation'])

        for breeding in breedings:
            best_result = [0]
            for i in range(5):
                print(f"{breeding}-{i}")
                test = GeneticAlgorithm(graph, 200, 10000, 10000, 0.3, False, 'elitism', breeding).run(graph)

                if test[-1] > best_result[-1]:
                    best_result = test

            for i, score in enumerate(best_result):
                writer.writerow([breeding, score, i])

            plt.plot(range(len(best_result)), best_result, label=breeding)
    
    plt.legend()
    plt.title(f'Scores for different breeding strategies (n = 5, scale = Nationaal)')
    plt.xlabel('# Generation')
    plt.ylabel('Score')
    plt.show()

            
def plot_mutation(csv_file):

    with open(csv_file, 'r') as csv_file:
        reader = csv.DictReader(csv_file)

        mr = []
        scores = []
        for line in reader:
            mr.append(float(line['mutation_rate']))
            scores.append(float(line['score']))

    plt.plot(mr, scores)
    plt.title(f'Scores for different mutation rates (n = 5, scale = Nationaal)')
    plt.xlabel('Mutation rate')
    plt.ylabel('Score')
    plt.show()