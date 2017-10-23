# Long Term Assignment 1
---

## Why
This is a long term assignment for CS350 at Boston University for Professors Bestavros &amp; Mancuso.

## How to run
This program is written in Python 3 and will not perform correctly in Python 2.7.
This program also uses a few various libraries including numpy, matplotlib, and random. Additionally, it uses some other useful Python libraries such as Queue and heapq which are important for modeling the M/M/1 system. Each file uses at least one of the other files, except part1.py which uses none, so they must all be in the same directory.

### part1.py
Simply running the program through the command line with:
~~~
python3 part1.py
~~~
This will generate the two graphs and calculate a different simulation every time.

### part2.py
Part 2 is a little a more complex as it takes advantage of command line arguments.
To get help with the command line arguments you can type:
~~~
python3 part2.py -h
~~~
Then you can type in the numbers you want to use for lambda, Ts and simulation time as follows:

~~~
python3 part2.py -l 5 -t 0.15 -s 1000
~~~
It will then run the program for the simulation time of 1000.

### part3.py
Part 3 only requires you to run it through the command line and will automatically generate the plot for the table given in the Part 3 section of LT1.
Simply running the program through the command line with:
~~~
python3 part3.py
~~~

### part4.py
Due to the complexity of this part, Part 4 is limited in the sense that all the simulation numbers are hard programmed into the main() function. This could be adapted to allow a more malleable and useful program in the future, but given the time constraints it is more unrealistic at the moment. To run the program simply do this:
~~~
python3 part4.py
~~~
This part simply returns two lists, the first being a set of average customers in each queue for the five queue system. The second, is the utilitizations for each M/M/1 queue in the system.
