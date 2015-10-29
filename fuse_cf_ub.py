from __future__ import division
from operator import itemgetter

import csv
import math

# Import stuff from other files.
import formula_list as fl
import fuse_cf_utility as fcu
import input_spreadsheet_vector as isv

formulas = fl.get_formula_list()

csv_file_fuse = 'fuse_formula_count.csv'

# Set of base formula frequency from the Fuse corpus, with row id for each instance.
base_ff_set = []

# Set of all vectors from the Fuse corpus, with weighted formula-frequency
# inverse instance frequency (ff-iif) data for each formula.
vector_set = []

# Dictionary to hold the importance of formulas in Fuse by the proportion that uses it.
formula_imp_weight = {}

# Tuning constant for floating precision in weights.
tuning_factor = 1.0

# Testing instance, calculate all similarity values based on this.
testing_instance = []


# Loads the formula frequency from csv into the base set.
def load_base_ff_set():
    with open(csv_file_fuse, 'r') as f:
        csv_reader = csv.reader(f)
        csv_reader.next()

        for row in csv_reader:
            row_data = []
            for element in row:
                row_data.append(int(element))
            base_ff_set.append(row_data)

    # Add the testing instance at the very end.
    test = isv.get_testing_vector('Test.xlsx')
    base_ff_set.append(test)


def calculate_formula_weight():
    # Initialize formula weights.
    for formula in formulas:
        formula_imp_weight[formula] = 0.0

    for instance in base_ff_set:
        for index in xrange(0, len(formulas)):
            # First get the no. of instances that uses this formula.
            if instance[index] > 0:
                formula_imp_weight[formulas[index]] += 1

    # The weight dictionary has instance count by formula. Now calculate the weight.
    instances_with_formulas = len(base_ff_set)
    for key, value in formula_imp_weight.iteritems():
        if value > 0.0:
            value = math.log(instances_with_formulas/value)
            formula_imp_weight[key] = value


def calculate_weighted_vectors():
    for instance in base_ff_set:
        instance_total = sum(instance)
        instance_formula_weights = []
        for i in xrange(0, len(formulas)):
            instance_formula_weights.append(tuning_factor * (instance[i]/instance_total) *
                                            formula_imp_weight[formulas[i]])

        vector_set.append(instance_formula_weights)


def get_knn(n):
    # Separate the testing instance from the vector set.
    global testing_instance
    testing_instance = vector_set.pop()

    similarity_results = []
    for index in xrange(0, len(vector_set)):
        similarity_results.append([index, fcu.cosine_similarity(testing_instance, vector_set[index])])

    # Sort the similarity values, stored in position 1 of results.
    similarity_results = sorted(similarity_results, key=lambda k: k[1], reverse=True)

    return similarity_results[:n]


def get_recommendations(similars):
    recommendations = {}
    input_instance = base_ff_set.pop()
    for similar in similars:
        # The actual instance to recommend from.
        similar_instance = base_ff_set[similar[0]]

        # Sanity check
        assert (len(formulas) == len(similar_instance)), "The similar instance doesn't have correct dimension"
        for index in xrange(0, len(formulas)):
            formula = formulas[index]
            if input_instance[index] == 0 and similar_instance[index] > 0:
                if formula in recommendations:
                    recommendations[formula] += similar_instance[index]
                else:
                    recommendations[formula] = similar_instance[index]

    recommendations_sorted = sorted(recommendations.items(), key=itemgetter(1), reverse=True)

    # Return only the list of formulas.
    return [item[0] for item in recommendations_sorted]


def main():
    load_base_ff_set()

    calculate_formula_weight()

    calculate_weighted_vectors()

    results = get_knn(3)

    recommendations = get_recommendations(results)

    print recommendations

    return 0

if __name__ == '__main__':
    main()
