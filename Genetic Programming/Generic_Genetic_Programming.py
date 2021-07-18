# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 15:15:20 2021

@author: Shishir Khanal
CAES Summer Bootcamp 2021
Presenter: Dr Paul Bodily 
"""
import random

POPULATION_SIZE = 10
CHILD_COUNT = 10
GENERATION_COUNT = 100

def initialize_individual():
    return "solution"

def crossover(parents):
    return "crossover result"

def mutate(child):
    return "mutated child"

def score_fitness(individual):
    return 100

def initialize_population():
    population = []
    
    for i in range(POPULATION_SIZE):
        individual = initialize_individual()
        fitness_score = score_fitness(individual)
        population.append((individual, fitness_score))
    return population


def run_genetic_algorithm():
    #START
    #Generate initial population
    population = initialize_population()
    #Compute fitness
    #Repeat
    for generation in range(POPULATION_SIZE):
        print("Generation", generation)
        print(population)
        children = []
        for i in range(CHILD_COUNT):
            #Selection
            parents = random.sample(population, 2)
            #Crossover
            child = crossover(parents)
            #Mutation
            child = mutate(child)
            #Compute Fitness
            fitness_score = score_fitness(child)
            children.append((child, fitness_score))
            #Prune Population
            population.sort(key=lambda x: x[1], reverse = True)
            population = population[:POPULATION_SIZE]
            
        population += children

        # UNTIL population has averaged
        #Stop
        return population[0]

if __name__ == '__main__':
    bestsolution = run_genetic_algorithm()
    print(bestsolution)