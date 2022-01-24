# -----------------------------------------------------------
# genetic.py
#
# Class definition of a Genetic Algorithm 
#
# Authors: Sam Bijhouwer and Maik Larooij
# -----------------------------------------------------------

import random

from code.classes.routemap import Routemap
from .randomise import generate_random_route
from .constants import get_constants

class GeneticAlgorithm():
    """ 
    Implements a genetic algorithm, insipred by the process of natural selection.

    Arguments:
    - graph: the input graph with all the stations and connections
    - generations: the number of times to repeat the selection, crossover and mutation phase
    - genes_size: the number of different random genes (routes) to generate
    - population_size: the number of different combinations of genes to generate a population
    - mutation_rate: the chance for mutation to happen, 0.2 means 20% chance of mutation
    """

    def __init__(self, graph, generations, genes_size, population_size, mutation_rate):
        self.graph = graph
        self.max_time, self.max_routes = get_constants(graph.scale)
        self.generations = generations
        self.genes_size = genes_size
        self.population_size = population_size
        self.mutation_rate = mutation_rate

    def generate_genes(self):
        """
        Generates genes based on the user inputted gene size of the algorithm.
        A gene maps back to a randomly constructed single route object.
        """
        return [generate_random_route(self.graph, self.max_time) for _ in range(self.genes_size)]

    def return_random_population(self):
        """
        Generates a population to start the algorithm with.
        A population consists of chromosomes (= random combination of route objects, or genes). 
        A chromosome consists of genes (= randomly generated route objects)
        """
        # Generate genes
        self.genes = self.generate_genes()
        
        # Randomly create combinations of genes
        self.start_population = [[random.choice(self.genes) for _ in range(random.randint(1, self.max_routes))] for _ in range(self.population_size)]

        return self.start_population

    def calculate_fitness(self, population):
        """ 
        Calculates the fitness of all chromosomes (combinations of routes) in the population.
        The fitness is the score of the routemap.
        """
        fitness = []
        for chromosome in population:

            # Create a routemap with all routes in this chromosome
            routemap = Routemap()
            for gene in chromosome:
                routemap.add_route(gene)

            # Calculate the score of this chromosome
            score = routemap.calc_score(len(self.graph.connections))
            fitness.append((chromosome, score))
        
        # Return a sorted list of all scored chromosomes
        return [chromosome[0] for chromosome in sorted(fitness, key=lambda x: x[1], reverse=True)]

    def select(self, population, place_to_cut):
        """
        Returns a cut population, while preserving the original size.
        """
        new_population = [None for _ in range(len(population))]
        new_population[0:place_to_cut] = population[0:place_to_cut]

        return new_population

    def crossover(self, population):
        """
        Combines two parents to create new children.
        Replaces half of the population by these newly made children.
        """
        
        # Select half the population
        halfway = int(len(population) / 2)
        new_population = self.select(population, halfway)

        for i in range(halfway, len(population)):

            # Randomly choose two parents
            first_parent = population[random.randint(0, halfway)]
            second_parent = population[random.randint(0, halfway)]

            # Randomly choose a crossover point
            crossover_point = random.randint(0, min([len(parent) for parent in [first_parent, second_parent]]) - 1)

            # Combine parents into new child
            child = first_parent[:crossover_point] + second_parent[crossover_point:]
            new_population[i] = child
        
        return new_population

    def mutate(self, population):
        """ 
        Mutate a chromosome based on chance.
        A mutation means that a route is replaced by a random route from the start genes.
        """
        for chromosome in population:
            if random.random() < self.mutation_rate:
                
                # Mutation, insert new random route
                mutate_index = random.randint(0, len(chromosome) - 1)
                chromosome[mutate_index] = random.choice(self.genes)
        
        # Return mutated population
        return population

    def run(self, graph):
        """ 
        Runs the genetic algorithm
        """
        
        # Create start population and calculate fitness
        population = self.return_random_population()
        fitness_pop = self.calculate_fitness(population)

        # Go on until number of generations is reached
        for _ in range(self.generations):
            
            # Crossover https://en.wikipedia.org/wiki/Crossover_(genetic_algorithm)
            crossed_population = self.crossover(fitness_pop)

            # Mutation https://en.wikipedia.org/wiki/Mutation_(genetic_algorithm)
            mutated_population = self.mutate(crossed_population)

            # Calculate the fitness of the end population
            fitness_pop = self.calculate_fitness(mutated_population)

        # Create a routemap of the best option after all generations
        routemap = Routemap()
        for route in fitness_pop[0]:
            routemap.add_route(route)

        return routemap