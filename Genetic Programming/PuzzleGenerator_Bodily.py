'''
Creating crossword mini puzzles using a genetic algorithm and a wordnet-based fitness function

Written by Paul Bodily for CS 4473, Computational Creativity
Python version 3.9.1
'''

from nltk.corpus import wordnet
import random
import string

DIMENSION = 4  # Puzzle dimension (both width and height)
MUTATION_RATE = 0.05
MAX_SCORE = DIMENSION * 2


def print_crossword(crossword_to_print):
    for row in crossword_to_print:
        for letter in row:
            print(letter, " ", end='')
        print()


def initialize_crossword():
    return [[random.choice(string.ascii_uppercase) for i in range(DIMENSION)] for j in range(DIMENSION)]


def initialize_population(population_size):
    population = []
    for i in range(population_size):
        new_crossword = initialize_crossword()
        population.append((new_crossword, calculate_fitness(new_crossword)))

    return population


def crossover(parent1_crossword, parent2_crossword):
    return [[parent1_crossword[j][i] if i > j else parent2_crossword[j][i] for i in range(DIMENSION)] for j in range(DIMENSION)]


def mutate_in_place(crossword_to_mutate):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            if random.random() < MUTATION_RATE:
                crossword_to_mutate[i][j] = random.choice(string.ascii_uppercase)


def calculate_fitness(crossword_to_eval):
    score = 0
    words_seen = set()

    # Words in rows
    for i in range(DIMENSION):
        word = ''.join(crossword_to_eval[i])
        if word not in words_seen and wordnet.synsets(word):
            words_seen.add(word)
            score += 1

    # Words in cols
    for j in range(DIMENSION):
        word = ''
        for i in range(DIMENSION):
            word += crossword_to_eval[i][j]
        if word not in words_seen and wordnet.synsets(word):
            words_seen.add(word)
            score += 1

    return score


def run_ga(gens, population_size=20, children_per_generation=20):
    population = initialize_population(population_size)

    for gen in range(gens):
        print("START GENERATION", gen+1)
        children = []
        for i in range(children_per_generation):
            parents = random.sample(population, 2)
            child = crossover(parents[0][0], parents[1][0])
            mutate_in_place(child)

            children.append((child, calculate_fitness(child)))

        population += children

        population.sort(key=lambda x: x[1], reverse=True)

        population = population[:population_size]

        print("Best Crossword after generation", gen, ":")
        print_crossword(population[0][0])
        print("Fitness:", population[0][1])

        if population[0][1] >= MAX_SCORE:
            break

    return population, gen+1


def print_crossword_clues(crossword_to_clue):
    for i in range(DIMENSION):
        word = ''.join(crossword_to_clue[i])
        syns = wordnet.synsets(word)
        if syns:
            print(i+1, "Across:", syns[0].definition(), "(", word, ")")
        else:
            print(i+1, "Across:", word, "is invalid")

    print()

    # Words in cols
    for j in range(DIMENSION):
        word = ''
        for i in range(DIMENSION):
            word += crossword_to_clue[i][j]
        syns = wordnet.synsets(word)
        if syns:
            print(j+1, "Down:", syns[0].definition(), "(", word, ")")
        else:
            print(j+1, "Down:", word, "is invalid")


if __name__ == '__main__':
    generations = 10000
    crosswords, gen_count = run_ga(gens=generations, population_size=10)

    print(gen_count, "generations (out of", generations, "allowed) complete. Printing result:")
    best_crossword = crosswords[0]
    print_crossword(best_crossword[0])
    print("Fitness:", best_crossword[1])
    print("Clues:")
    print_crossword_clues(best_crossword[0])
