from __future__ import division
import math

def euclidean_distance(v1, v2):
    assert (len(v1) == len(v2)), "The vectors don't have the same dimension"
    distance = sum([(i - j) ** 2 for i, j in zip(v1, v2)]) ** 0.5
    assert (distance >= 0), "Distance can't be less than 0"
    return distance

def cosine_similarity(v1, v2):
    assert (len(v1) == len(v2)), "The vectors don't have the same dimension"
    sum_x_square, sum_x_mult_y, sum_y_square = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sum_x_square += x*x
        sum_y_square += y*y
        sum_x_mult_y += x*y
    return 1 - (sum_x_mult_y / math.sqrt(sum_x_square * sum_y_square))
