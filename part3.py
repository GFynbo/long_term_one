#
# Gavin Fynbo
# fynbo@bu.edu
# U54777118
#
# This is part3 of the first Long Term Assignment in
# Boston University CAS CS350.
# Prof. Bestavros & Prof. Mancuso
#

from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import random

def customDistr(table):
    ''' takes a well formed table and creates a custom distribution based on
        said table '''

    # initialize new table and value
    prob_dist = [[0,0] for i in range(len(table))]
    val = random.random()

    # initialize the first set
    prob_dist[0][0] = table[0][1]
    prob_dist[0][1] = table[0][0]
    # update all values
    for i in range(1,len(table)):
        prob_dist[i][0] = table[i][1] + prob_dist[i-1][0]
        prob_dist[i][1] = table[i][0]

    # find value based on dist and random var
    for i in range(len(prob_dist)):
        if val <= prob_dist[i][0]:
            return prob_dist[i][1]
        else:
            continue

def main():
    ''' RUN AND TEST THE PROGRAM '''
    test_table = [[5, 0.03], [10, 0.13], [20, 0.22], [40, 0.12], [70, 0.17], [100, 0.08], [110, 0.20], [115, 0.05]]
    test_results = []

    for i in range(1000):
        test_results += [customDistr(test_table)]

    test_results = Counter(test_results)
    # y_vals = [x for x in test_results]
    x_vals = [x[0] for x in test_table]
    y_vals = [test_results[x]/1000 for x in x_vals]
    plt.plot(x_vals, y_vals)
    plt.ylabel('Probability')
    plt.xlabel('Value')
    plt.title('Custom Distribution PDF')
    plt.show()

if __name__ == "__main__":
    main()
