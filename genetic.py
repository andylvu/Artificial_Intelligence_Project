import numpy as np
import pandas as pd

'''
"fitness" calculates the fitness of the speciments in the population.
Returns an array of fitness scores, which is the value achieved given the threshold was not exceeded.
'''


def fitness(population, values, costs, threshold):
    specimen_values = np.zeros(shape=(len(population))).astype(int)
    specimen_costs = np.zeros(shape=(len(population))).astype(int)

    # Iterate over all speciments in the population
    for i in range(len(population)):
        # The total value of all items in ith specimen of the population
        specimen_values[i] = np.sum(population[i] * values)
        # The total cost of all items in the ith specimen
        specimen_costs[i] = np.sum(population[i] * costs)

    # Filter only value totals that fit within threshold
    specimen_values[specimen_costs > threshold] = 0

    return specimen_values


'''
"Parent_selection" determines which specimens in the population are suitable for reproduction based on fitness scores.
The function finds the best half of the population and returns them as an array parents.
In the event that there are no fit parents, np.argsort will simply select the indices of the middle half of the population.
    This will also be the case in selecting supplementary parents if less than half are fit.

Note that population count MUST be even, otherwise int() will round down
'''


def parent_selection(fitness_score, population):
    # Half of the population
    number_of_parents = int(len(population) / 2)

    # Get array of indices for parents selected as candidates
    candidate_indices = np.argsort(fitness_score)[::-1][:number_of_parents]

    return population[candidate_indices]


'''
"cross_breeding" takes half of one specimen's genes and mixes them with another.
Two offspring are 'born' for each pair of parents, each containing half of each parents genes.
The two offspring's inhereted genes are not the same, as they are taken from opposite halves of the parent's.
Parents are mated in decending order, if there are 4 parents, there will be 4 offspring, 2 to each pair.
This returns a new array of offspring
If the number of parents is odd, the last parent will produce a single offspring with the most fit parent.
'''


def cross_breeding(parents):
    # make array of offspring, same shape as parents
    offspring = np.zeros(parents.shape).astype(int)

    # Crossover point is half of the 'genes' (items in the database), it is rounded down if odd.
    cp = int(len(parents[0]) / 2)

    # Case that the number of offspring is even
    if len(offspring) % 2 == 0:
        for i in range(0, len(offspring), 2):
            # First offspring
            offspring[i][:cp] = parents[i][:cp]
            offspring[i][cp:] = parents[i + 1][cp:]

            # Second offspring
            offspring[i + 1][:cp] = parents[i + 1][:cp]
            offspring[i + 1][cp:] = parents[i][cp:]

    # Case that the number of offspring is odd
    else:
        for i in range(0, len(offspring) - 1, 2):
            # First offspring
            offspring[i][:cp] = parents[i][:cp]
            offspring[i][cp:] = parents[i + 1][cp:]

            # Second offspring
            offspring[i + 1][:cp] = parents[i + 1][:cp]
            offspring[i + 1][cp:] = parents[i][cp:]

        # Final, odd numbered, offspring from the both the worst and best parents
        offspring[len(offspring) - 1][:cp] = parents[len(offspring) - 1][:cp]
        offspring[len(offspring) - 1][cp:] = parents[0][cp:]

    # Return mutated offspring
    return induce_mutations(offspring)


'''
"Induce_mutations" adds mutations at a low rate to the offspring of the current generation.
This works a bit sign flip, changing one or more genes where a mutation is set to occur.
This is done through generating floats between 1 and 0, and using a rate of mutation as a float.
When a number is below or at the rate of mutation, the gene at that index is set to mutate.
'''


def induce_mutations(offspring):
    # Declare a rate of mutation, the change at which a mutation will occur as a percentage
    mutation_rate = 0.1

    # Make a copy of offspring
    mutated_offspring = np.copy(offspring)

    # Declare RNG
    random_gen = np.random.default_rng()

    for i in range(len(mutated_offspring)):

        # Generate random numbers between 1 and 0, those below mutation rate will be mutated
        mutant_gene_chance = random_gen.random((len(mutated_offspring[0])))

        # Indices where mutations will occur
        mutant_indices = np.argwhere(mutant_gene_chance <= mutation_rate)

        # Case that mutants will occur
        if len(mutant_indices) != 0:
            for m in mutant_indices:
                # Flip sign of the gene at that index
                mutated_offspring[i, m] = 1 - mutated_offspring[i, m]

    return mutated_offspring


'''
Simple helper function to combine arrays
'''


def zip_arrays(population, parents, offspring):
    new_population = np.copy(population)

    half = int(len(new_population) / 2)

    new_population[:half] = parents
    new_population[half:] = offspring

    return new_population


'''
Generates an initial population based on the percentage of threshold/sum of all costs.
This allows for scaling for very low or veryhigh thresholds
If the threshold is too low, the population will never generate a specimen that is below threshold.
This addresses that issue.
E.g., if threshold is 5% of total costs, ~5% of items will be in the specimens.
Works similar to the induce_mutation function
'''


def initial_population_generation(population_size, produce, costs, threshold):
    # Get the pecentage of items that should be in the specimens
    max_total_cost = int(np.ceil(np.sum(costs)))
    threshold_percentage = threshold / max_total_cost

    # build initial pop as zeros
    initial_population = np.zeros(shape=(population_size, len(produce))).astype(int)

    # Declare RNG
    random_gen = np.random.default_rng()

    # Iterage over all specimens
    for i in range(len(initial_population)):
        # Generage percentages that the item at this index will be included
        inclusion_chance = random_gen.random((len(initial_population[0])))

        # Flip 0 to 1 where the inclusion chance is below the threshold percentage
        initial_population[i, inclusion_chance <= threshold_percentage] = 1

    return initial_population


'''
function for rounding total price up to two decimal points
'''


def round_up_2_decimals(a):
    return np.round(a + 0.5 * 10 ** (-2), 2)


'''
main function
'''


def genetic_main(initial_population, costs, values, threshold, population_size, generations):
    current_population = initial_population
    for i in range(generations):
        current_fitness_score = fitness(current_population, values, costs, threshold)
        current_parents = parent_selection(current_fitness_score, current_population)
        current_offspring = cross_breeding(current_parents)
        current_population = zip_arrays(current_population, current_parents, current_offspring)

    final_gen_fitnesses = fitness(current_population, values, costs, threshold)

    return current_population[np.argmax(final_gen_fitnesses)]

def test(budgetAmount):
    # Import csv as dataframe
    items = pd.read_csv("groceries.csv")

    # Get numpy arrays from each of the columns
    produce = items['Food'].to_numpy().astype('str')
    costs = items['Price'].to_numpy().astype('float64')
    values = items['weight (lbs)'].to_numpy().astype('float64')

    threshold = int(budgetAmount)

    population_size = 16
    # Create initial population, each individual specimen is binary encoded
    # Encoding is if item at that index is included in the specimen
    initial_population = initial_population_generation(population_size, produce, costs, threshold)
    generations = 50

    output = genetic_main(initial_population, costs, values, threshold, population_size, generations)

    # Print list of produce that has been selected
    print(produce[output == 1])

    # Print total price
    print(round_up_2_decimals(np.sum(costs[output == 1])))

    # Print total value of the list
    print(np.sum(values[output == 1]))
    return produce[output == 1], round_up_2_decimals(np.sum(costs[output == 1]));