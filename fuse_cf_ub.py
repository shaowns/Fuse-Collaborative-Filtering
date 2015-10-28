from __future__ import division

import csv
import math

# Import stuff from other files.
import formula_list as fl
import fuse_cf_utility as fcu
import input_spreadsheet_vector as isv

formulas = fl.get_formula_list()

csv_file_fuse = 'fuse_formula_count.csv'

# Set of all vectors from the Fuse corpus, with formula-frequency
# inverse instance frequency (ff-iif) data for each formula.
vector_set = []

# Dictionary to hold the importance of formulas in Fuse by the proportion that uses it.
formula_imp_weight = {}

# Tuning constant for floating precision in weights.
tuning_factor = 1.0

# Testing instance, calculate all similarity values based on this.
testing_instance = []


def initialize_formula_imp_weights():
    for formula in formulas:
        formula_imp_weight[formula] = 0.0


def load_vector_set():
    with open(csv_file_fuse, 'r') as f:
        csv_reader = csv.reader(f)
        csv_reader.next()
        for row in csv_reader:
            row_data = []
            for element in row:
                row_data.append(int(element))
            vector_set.append(row_data)

    # Add the testing instance at the very end.
    test = isv.get_testing_vector('Test.xlsx')
    vector_set.append(test)


def calculate_formula_weight():
    initialize_formula_imp_weights()
    for instance in vector_set:
        for index in xrange(0, len(formulas)):
            # First get the no. of instances that uses this formula.
            if instance[index] > 0:
                formula_imp_weight[formulas[index]] += 1

    # The weight dictionary has instance count by formula. Now calculate the weight.
    instances_with_formulas = len(vector_set)
    for key, value in formula_imp_weight.iteritems():
        if value > 0.0:
            value = math.log(instances_with_formulas/value)
            formula_imp_weight[key] = value


def calculate_formula_vectors():
    for i in xrange(0, len(vector_set)):
        instance = vector_set[i]
        instance_total = sum(instance)

        for j in xrange(0, len(formulas)):
            cur_formula = formulas[j]
            instance[j] = tuning_factor * (instance[j]/instance_total) * formula_imp_weight[cur_formula]

        vector_set[i] = instance


def get_knn(n):
    global testing_instance
    testing_instance = vector_set.pop()

    similarity_results = []
    for instance in vector_set:
        similarity_results.append([instance, fcu.cosine_similarity(testing_instance, instance)])

    # Sort the similarity values, stored in position 1 of results.
    similarity_results = sorted(similarity_results, key=lambda k: k[1], reverse=True)

    return similarity_results[:n]


def get_recommendations(recommendation_instances, n):
    recommendations = []
    for i in xrange(0, n):
        # The actual instance to recommend from.
        instance = recommendation_instances[i][0]

        # Sanity check
        assert (len(formulas) == len(instance)), "The similar instance doesn't have correct dimension"
        assert (len(testing_instance) == len(instance)), "The similar instance doesn't have correct dimension"

        for index in xrange(0, len(formulas)):
            if testing_instance[index] == 0.0 and instance[index] > 0.0:
                recommendations.append(formulas[index])

    return recommendations


def main():
    load_vector_set()

    calculate_formula_weight()

    calculate_formula_vectors()

    results = get_knn(3)

    recommendations = get_recommendations(results, 3)

    print recommendations

    return 0

if __name__ == '__main__':
    main()
