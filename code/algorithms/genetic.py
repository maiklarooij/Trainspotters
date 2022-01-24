from .randomise import generate_random_route
from code.classes.routemap import Routemap
from .constants import get_constants

import random

class GeneticAlgorithm():

    def __init__(self, graph, generations, genes_size, population_size, mutation_rate):
        self.graph = graph
        self.max_time, self.max_routes = get_constants(graph.scale)
        self.generations = generations
        self.genes_size = genes_size
        self.population_size = population_size
        self.mutation_rate = mutation_rate

    def generate_genes(self):

        return [generate_random_route(self.graph, self.max_time) for _ in range(self.genes_size)]

    def return_random_population(self):

        self.genes = self.generate_genes()
        self.start_population = [[random.choice(self.genes) for _ in range(random.randint(1, self.max_routes))] for _ in range(self.population_size)]

        return self.start_population

    def calculate_fitness(self, population):

        fitness = []
        for chromosome in population:

            routemap = Routemap()
            for gene in chromosome:
                routemap.add_route(gene)

            score = routemap.calc_score(len(self.graph.connections))
            fitness.append((chromosome, score))
        
        return [chromosome[0] for chromosome in sorted(fitness, key=lambda x: x[1], reverse=True)]

    def select(self, population, place_to_cut):

        new_population = [None for _ in range(len(population))]
        new_population[0:place_to_cut] = population[0:place_to_cut]

        return new_population

    def crossover(self, population):
        
        halfway = int(len(population) / 2)
        new_population = self.select(population, halfway)

        for i in range(halfway, len(population)):
            first_parent = population[random.randint(0, halfway)]
            second_parent = population[random.randint(0, halfway)]

            crossover_point = random.randint(0, min([len(parent) for parent in [first_parent, second_parent]]) - 1)

            child = first_parent[:crossover_point] + second_parent[crossover_point:]
            new_population[i] = child
        
        return new_population

    def mutate(self, population):

        for chromosome in population:
            if random.random() < self.mutation_rate:

                mutate_index = random.randint(0, len(chromosome) - 1)
                chromosome[mutate_index] = random.choice(self.genes)
        
        return population

    def run(self, graph):

        population = self.return_random_population()
        fitness_pop = self.calculate_fitness(population)

        for _ in range(self.generations):

            crossed_population = self.crossover(fitness_pop)
            mutated_population = self.mutate(crossed_population)

            fitness_pop = self.calculate_fitness(mutated_population)

        routemap = Routemap()
        for route in fitness_pop[0]:
            routemap.add_route(route)

        return routemap

        

            

    


