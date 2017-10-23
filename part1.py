#
# Gavin Fynbo
# fynbo@bu.edu
# U54777118
#
# This is part1 of the first Long Term Assignment in
# Boston University CAS CS350.
# Prof. Bestavros & Prof. Mancuso
#

import math
import random
import time
import numpy as np
import matplotlib.pyplot as plt

class RandVar():
    ''' This class is a culmination of methods and functions that will generate
        variables for specific distributions '''

    def __init__(self, lam=1, num_trials=1000):
        ''' initialize the class with the proper variables '''
        self.n = num_trials
        self.vals = []
        self.lam = lam
        self.mu = 0

    def exp(self, test=-1):
        ''' that uses a uniform random generator and returns a random value that is distributed according
            to an exponential distribution with a mean of T = 1/lambda. '''
        # generate random num [0, 1) for the distribution
        random_num = random.random()
        if (test <= -1):
            test = self.lam

        # computes the value using the math library for natural log and finding the ln(1 - the random var)
        # from there is then divides that by negative of the
        x = math.log(1 - random_num) / (test * -1)
        return x

    def generate_values(self):
        ''' generates a list of values for a given lambda and number of trials '''
        self.vals = [self.exp() for i in range(self.n)]
        return

    def find_mean_generate(self):
        ''' find and generate various useful probability values such as mean and stddev '''
        if (self.vals == []):
            self.generate_values()

        # calculate mu (average/mean)
        self.mu = sum(self.vals) / len(self.vals)
        return

    def print_vals(self):
        ''' simple print out a list of the vals generated '''
        for i in range(len(self.vals)):
            print(str(i) + ": " + str(self.vals[i]))

    def generate_CDF_both(self):
        ''' this function generates and prints a CDF plot of Empirical vs. Analytical '''
        data = self.vals
        t = np.arange(0.0, 2.0, 0.01)
        sorted_data = np.sort(data)
        analytical = 1 - (math.e ** (-1 * self.lam * t))

        yvals=np.arange(len(sorted_data))/float(len(sorted_data)-1)

        plt.plot(sorted_data,yvals, lw=2, label="Empirical")
        plt.plot(t, analytical, lw=1.5, label="Analytical")
        plt.title('Empirical v. Analytical Distribution')
        plt.ylabel('Cumulative Probability')
        plt.xlabel('Value')
        plt.legend(loc=4, borderaxespad=0.)

        plt.show()

    def generate_CDF_single(self):
        ''' this function generates and prints a CDF plot of the given values Empirically'''
        data = self.vals
        sorted_data = np.sort(data)

        yvals=np.arange(len(sorted_data))/float(len(sorted_data)-1)

        plt.plot(sorted_data,yvals, lw=2, label="Empirical")
        plt.title('Empirical Distribution')
        plt.ylabel('Cumulative Probability')
        plt.xlabel('Value')
        plt.legend(loc=4, borderaxespad=0.)

        plt.show()



def main():
    # TESTING OF CODE

    test = RandVar(4, 1000)
    test.find_mean_generate()

    test.print_vals()
    print(test.mu)
    test.generate_CDF_single()
    test.generate_CDF_both()

if __name__ == "__main__":
    main()
