"""
Created on Wed Jul 14 15:45:20 2021

@author: Shishir Khanal
CAES Summer Bootcamp 2021
Presenter: Dr Paul Bodily 
"""

import random
import string

MUTATION_RATE = 0.25
POPULATION_SIZE = 10
CHILD_COUNT = 10
GENERATION_COUNT = 100
SOLUTION = "optimality"

def initialize_individual():
    #List Comprehension
    return [random.choice(string.ascii_lowercase) for i in range(len(SOLUTION))]


def score_fitness(individual):
    fitness_score = 0
    for i in range(len(individual)):
        if individual[i] == SOLUTION[i]:
            fitness_score += 1
    return fitness_score


def initialize_population():
    population = []

    for i in range(POPULATION_SIZE):
        individual = initialize_individual()
        fitness_score = score_fitness(individual)
        population.append((individual, fitness_score))
    return population


def crossover(parents):
    parent_a = parents[0][0]
    parent_b = parents[1][0]
    child = []

    for i in range(len(SOLUTION)):
        if random.random() < 0.5:
            child.append(parent_a[i])
        else:
            child.append(parent_b[i])
    return child


def mutate(child):
    for i in range(len(SOLUTION)):
        if random.random() < MUTATION_RATE:
            child[i] = random.choice(string.ascii_lowercase)
    return child


def run_genetic_algorithm():
    # START
    # Generate the initial population; each individual is a (genome, score)
    population = initialize_population()
    # Compute fitness
    # REPEAT
    children = []
    for generation in range(GENERATION_COUNT):
        print("Generation", generation)
        for i in range(CHILD_COUNT):
            # Selection
            parents = random.sample(population, 2)
            print("parents",parents)
            # Crossover
            child = crossover(parents)
            print("child",child)
            # Mutation
            child = mutate(child)
            print("child",child)
            # Compute fitness
            fitness_score = score_fitness(child)
                
    population += children
        # Prune population
    population.sort(key=lambda x: x[1], reverse=True)
    population = population[:POPULATION_SIZE]

    # UNTIL population has converged
    # STOP
    return population[0]

if __name__ == '__main__':
    best_solution = run_genetic_algorithm()
    print(best_solution)