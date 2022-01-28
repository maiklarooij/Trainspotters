# -----------------------------------------------------------
# genetic.py
#
# Class definition of a Genetic Algorithm 
#
# Authors: Sam Bijhouwer and Maik Larooij
# -----------------------------------------------------------

import random
from code.algorithms.hillclimber import hillclimber_solution

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
    - use_hillcimber: boolean if hillclimber should be used in mutation phase
    - selection_strat: the selection strategy (options = 'elitism', 'rws', 'tournament')
    - breeding_strat: the breeding strategy (options = '1point', '2point', 'uniform')
    """

    def __init__(self, graph, generations, genes_size, population_size, mutation_rate, use_hillclimber, selection_strat, breeding_strat):
        self.graph = graph
        self.max_time, self.max_routes = get_constants(graph.scale)
        self.generations = generations
        self.genes_size = genes_size
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.use_hillclimber = use_hillclimber
        self.selection_strat = selection_strat
        self.breeding_strat = breeding_strat

        self.generations_results = []

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
        self.start_population = [([random.choice(self.genes) for _ in range(random.randint(1, self.max_routes))], 0) for _ in range(self.population_size)]

        return self.start_population

    def calculate_fitness(self, population):
        """ 
        Calculates the fitness of all chromosomes (combinations of routes) in the population.
        The fitness is the score of the routemap.
        """
        fitness = []
        for chromosome, score in population:
            
            # Calculate score
            score = self.calculate_fitness_chrom(chromosome)
            fitness.append((chromosome, score))
        
        # Return a sorted list of all scored chromosomes
        return sorted(fitness, key=lambda x: x[1], reverse=True)

    def calculate_fitness_chrom(self, chromosome):
        """
        Calculates the fitness of a single chromosome
        """ 
        routemap = Routemap()
        for gene in chromosome:
            routemap.add_route(gene)

        score = routemap.calc_score(self.graph.total_connections)

        return score

    def accumulate_scores(self, scores):
        """ 
        Returns for all the scores the accumulated value.
        Score of the last chromosome should be 1.
        """
        total_fitness = sum([score for chromosome, score in scores])

        acc_fitness = []
        cumulative_score = 0
        for chromosome, score in scores:

            # Normalize scores and count up
            normalized_score = score / total_fitness
            cumulative_score += normalized_score

            acc_fitness.append((chromosome, cumulative_score))

        return acc_fitness
        
    def select_elitism(self, population, place_to_cut):
        """
        Returns a cut population, while preserving the original size.
        Selects based on elitism, best individuals from the generation are carried over.
        """
        new_population = [None for _ in range(len(population))]
        new_population[0:place_to_cut] = population[0:place_to_cut]

        return new_population

    def select_rws(self, population, halfway):
        """
        Returns a cut population, while preserving the original size.
        Selects based on a roulette wheel, proportional to fitness.
        """

        new_population = [None for _ in range(len(population))]

        # Calculate total score of all chromosomes
        # total_scores = []
        # for chromosome, score in population:
        #     score = self.calculate_fitness_chrom(chromosome)
        #     total_scores.append((chromosome, score))

        # Accumulate all scores
        acc_fitness = self.accumulate_scores(population)

        for i in range(halfway):
            roulette = random.random()

            # Pick the first chromosome where the accumulated score is higher than the roulette value
            for chromosome, acc_score in acc_fitness:
                if acc_score >= roulette:
                    new_population[i] = (chromosome, 0)
                    break
            
        return new_population

    def select_tournament(self, population, halfway):

        new_population = [None for _ in range(len(population))]
        
        for i in range(halfway):
            
            selected = sorted(random.choices(population, k=int(len(population) / 10)), key=lambda x: x[1])

            new_population[i] = selected[0]
        
        return new_population

    def crossover(self, population, selection='elitism', breeding='1point'):
        """
        Combines two parents to create new children.
        Replaces half of the population by these newly made children.
        Options: 
        - selection: choose selection strategy
        - breeding: choose breeding strategy
        """
        
        # Different selection strategies
        selection_options = {'elitism': self.select_elitism, 'rws': self.select_rws, 'tournament': self.select_tournament}

        # Select half the population
        halfway = int(len(population) / 2)
        new_population = selection_options[selection](population, halfway)

        # Fill other half with children
        for i in range(halfway, len(population)):
            
            # Randomly choose two parents
            first_parent = population[random.randint(0, halfway - 1)][0]
            second_parent = population[random.randint(0, halfway - 1)][0]

            # Breed based on the inputted option
            breeding_options = {'1point': self.breed_kpoint(first_parent, second_parent, k=1), 
                                '2point': self.breed_kpoint(first_parent, second_parent, k=2),
                                'uniform': self.breed_uniform(first_parent, second_parent)}
            child = breeding_options[breeding]
            
            # Add child to population
            new_population[i] = (child, 0)
        
        return new_population

    def breed_kpoint(self, first_parent, second_parent, k):
        """ 
        Breed two parents, producing a new child based on k-point breeding.
        k = number of crossover points to cut the parents.
        """
        # Randomly choose k crossover points and append last point
        crossover_points = sorted([random.randint(0, min([len(parent) for parent in [first_parent, second_parent]]) - 1) for k in range(k)])
        crossover_points.append(max([len(parent) for parent in [first_parent, second_parent]]))

        child = []
        pos = 0
        for i, k in enumerate(crossover_points):
            
            # Alternate parents
            parent = first_parent if i % 2 == 0 else second_parent
            # Add piece of parent to child
            child += parent[pos:k]
            
            # Keep lower bound of next slice 
            pos += k

        return child

    def breed_uniform(self, first_parent, second_parent):
        """
        Breed two parent, producing a new child based on uniform breeding.
        Every gene of the child is randomly picked from one of the two parents.
        """ 

        # How often do we need to flip a coin?
        child_length = max([len(parent) for parent in [first_parent, second_parent]])
        # Flip a coin!
        bits = [random.randint(0, 1) for _ in range(child_length)]

        child = []
        for i in range(child_length-1):
            
            # Choose appropriate parent according to coin flip
            parent = first_parent if bits[i] == 1 else second_parent

            # Add gene to child if gene exists at this place
            if i < len(parent):
                child.append(parent[i])

        return child

    def mutate(self, population, version):
        """ 
        Mutate a chromosome based on chance.
        A mutation means that a route is replaced by a random route from the start genes.
        """
        for i, chromosome in enumerate(population):
            if random.random() < self.mutation_rate:
                
                if version == 'hillclimber':
                    population[i] = (hillclimber_solution(self.graph, chromosome[0]).routes, 0)
                else:
                    # Mutation, insert new random route
                    chromosome_copy = chromosome[0]
                    if len(chromosome_copy) > 1:
                        mutate_index = random.randint(0, len(chromosome_copy) - 1)
                    else:
                        mutate_index = 0
                    chromosome_copy[mutate_index] = random.choice(self.genes)
                    population[i] = (chromosome_copy, 0)
                    #chromosome[mutate_index] = random.choice(self.genes)
        
        # Return mutated population
        return population

    def generate_routemap(self, routes):
        """Generates a routemap from a list of route objects"""
        routemap = Routemap()
        for route in routes:
            routemap.add_route(route)

        return routemap

    def run(self, graph):
        """ 
        Runs the genetic algorithm
        """
        
        # Create start population and calculate fitness
        population = self.return_random_population()
        fitness_pop = self.calculate_fitness(population)

        best_solution = (None, 0)

        # Go on until number of generations is reached
        for generation in range(1, self.generations + 1):
            
            print(f"{generation}, {self.generate_routemap(fitness_pop[0][0]).calc_score(self.graph.total_connections)}")
            # self.generations_results.append(self.generate_routemap(fitness_pop[0][0]).calc_score(self.graph.total_connections))

            # Hillclimber option
            if (generation % (self.generations / 10) == 0) and self.use_hillclimber:
                version = 'hillclimber'
            else:
                version = 'random'
            
            # Crossover https://en.wikipedia.org/wiki/Crossover_(genetic_algorithm)
            crossed_population = self.crossover(fitness_pop, self.selection_strat, self.breeding_strat)

            # Mutation https://en.wikipedia.org/wiki/Mutation_(genetic_algorithm)
            mutated_population = self.mutate(crossed_population, version)

            # Calculate the fitness of the end population
            fitness_pop = self.calculate_fitness(mutated_population)

            if fitness_pop[0][1] > best_solution[1]:
                best_solution = fitness_pop[0]

        # Create a routemap of the best option after all generations
        routemap = Routemap()
        for route in best_solution:
            routemap.add_route(route)

        return routemap