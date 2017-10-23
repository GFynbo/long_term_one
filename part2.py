#
# Gavin Fynbo
# fynbo@bu.edu
# U54777118
#
# This is part2 of the first Long Term Assignment in
# Boston University CAS CS350.
# Prof. Bestavros & Prof. Mancuso
#

import argparse
import heapq
from part1 import RandVar
import queue

# parser for dealing with the command line arguments
parser = argparse.ArgumentParser(description='Process an M/M/1 Simulation using a controller and world.' +
' Written by Gavin Fynbo, for use in BU CAS CS350')
parser.add_argument('-l', metavar='L', type=float, nargs='+',
                   help='a float for the lambda of the system')
parser.add_argument('-t', metavar='T', type=float, nargs='+',
                   help='a float for average time of service for the system')
parser.add_argument('-s', metavar='S', type=int, nargs='+',
                   help='an int for simulation run time')

class Event:
    ''' This is the class for the structure of the linked list/heap queue of events as to
        hold certain information to be accessed later. '''

    def __init__(self, time_arrival, function_name):
        ''' initialize the Event to get its information '''
        self.time_stamp = time_arrival
        self.function = function_name

class Request:
    ''' This is the class for the structure of the queue of requests as to
        hold certain information to be accessed later by the M/M/1 system. '''

    def __init__(self, time_arrival, time_start, time_end):
        ''' initialize the request to get its information '''
        self.time_arrival = time_arrival
        self.time_start = time_start
        self.time_end = time_end

class Controller:
    ''' This is the controller for the simulated M/M/1 queuing system. This controller
        keeps track of the global timer and global schedule. '''

    def __init__(self, lam, ts, sim_time):
        ''' initialize the variables, timer, etc '''
        # read user input to get lambda, time of serice, and simulation time here
        self.lam = lam
        self.ts = ts
        self.sim_time = sim_time

        # keep track of Ts, mean customers in queue
        self.monitor_file = open('monitor_results.txt', 'w')
        self.ts_list = []
        self.customer_list = []
        self.tq_list = []
        self.interarrival_list = []
        self.dist = RandVar(self.lam)

        # initialize controller main properties here
        self.time = 0
        self.monitor_time = 1
        self.world = None
        self.schedule = []
        self.initialize_state()
        self.initialize_schedule()
        self.main()

    def main(self):
        ''' this is the main function of our simulation controller. this function
            runs, keeps track, and schedules events using helper functions. '''

        # run the simulation here until time reaches simulation time
        while(self.time < self.sim_time):
            event = self.advance_time()
            if (event == None):
                print("BROKEN: NONE\n")
                exit()
            event = event[1]

            self.time = event.time_stamp

            # if birth call birth function
            if (event.function == "birth"):
                self.add_arrival_event()
            # if death call death function
            elif (event.function == "death"):
                self.add_depature_event()
            # if monitor call monitor function
            else:
                self.add_monitor_event()
                self.monitor_time += self.dist.exp(1)

    def initialize_state(self):
        ''' initialize the world of the simulation '''
        self.world = World(self.lam, self.ts)
        #while(self.t < self.sim_time):
        #    pass

    def initialize_schedule(self):
        ''' initialize the schedule of the simulation '''
        # get first birth and first death and push them onto the schedule
        first_birth = Event(self.world.next_arrival, 'birth')
        heapq.heappush(self.schedule, [first_birth.time_stamp, first_birth])
        first_death = Event(self.world.next_departure, 'death')
        heapq.heappush(self.schedule, [first_death.time_stamp, first_death])
        first_monitor = Event(self.monitor_time, 'monitor')
        heapq.heappush(self.schedule, [first_monitor.time_stamp, first_monitor])

    def add_arrival_event(self):
        ''' this function simply adds the next arrival event and departure event
            to the heapq at a time time_stamp '''
        birth = self.world.birth(self.time)
        self.interarrival_list += [birth[0]]
        if (len(birth) == 1):
            next_arrival_event = Event(birth[0] + self.time, 'birth')
            heapq.heappush(self.schedule, [next_arrival_event.time_stamp, next_arrival_event])
            return
        self.ts_list += [(birth[1] - birth[0])]
        next_arrival_event = Event(birth[0] + self.time, 'birth')
        heapq.heappush(self.schedule, [next_arrival_event.time_stamp, next_arrival_event])
        next_departure_event = Event(birth[1] + self.time, 'death')
        heapq.heappush(self.schedule, [next_departure_event.time_stamp, next_departure_event])

    def add_depature_event(self):
        ''' this function simply adds the next departure event to the heapq at a time time_stamp '''
        death = self.world.death()
        if (death != 10000):
            self.ts_list += [death[0]]
            self.tq_list += [self.time - death[1]]
            next_departure_event = Event(death[0] + self.time, 'death')
            heapq.heappush(self.schedule, [next_departure_event.time_stamp, next_departure_event])


    def add_monitor_event(self):
        ''' this method impliments a monitoring event that captures the system in
            its current state, including number of customers in the queue, the
            amount of departures and the amout of arrivals '''
        next_departure_event = Event(self.monitor_time, 'monitor')
        heapq.heappush(self.schedule, [next_departure_event.time_stamp, next_departure_event])
        stats = [self.world.customers_in_system.qsize(), self.world.num_arrivals, self.world.num_departures]
        self.customer_list += [stats[0]]
        self.monitor_file.write("Monitor at: " + str(self.time) + " \nCustomers in queue: " + str(stats[0]) + " \nArrivals: " + str(stats[1]) + " \nDepartures: " + str(stats[2]) + " \n\n")

    def advance_time(self):
        ''' this function dequeues the next event in the calendar and updates
            the world controller time and then '''
        if (len(self.schedule) > 0):
            return heapq.heappop(self.schedule)
        else:
            return None

class World:
    ''' This is the M/M/1 world simulator that runs a number of methods and functions
        to simulate an M/M/1 queue. '''

    def __init__(self, lam=1, ts=0.5):
        ''' initialize the world simulator for specific variables such as
            arrival rate, time to service and the total simulation time '''

        # for generating arrival and departure times
        self.lam = lam
        self.ts = ts

        # monitoring purposes
        self.num_arrivals = 0
        self.num_departures = 0

        # create the queue for M/M/1
        self.customers_in_system = queue.Queue()

        # for calculating the initial arrival and departure time
        self.dist = RandVar(self.lam)
        self.next_arrival = self.dist.exp()
        self.next_departure = self.next_arrival + self.dist.exp((1/self.ts))

    def birth(self, time_arrival=0):
        ''' the birth of an event to be added into M/M/1 Queue and the birth and
            death events to be added into the simulation schedule '''
        req = Request(time_arrival, time_arrival, -1)
        self.customers_in_system.put(req)
        self.num_arrivals += 1
        self.next_arrival = self.dist.exp(self.lam)
        if (self.customers_in_system.qsize() <= 1):
            self.next_departure = self.next_arrival + self.dist.exp((1/self.ts))
            return [self.next_arrival, self.next_departure]
        return [self.next_arrival]

    def death(self):
        ''' the death of an event to be removed from the M/M/1 Queue '''
        if (self.customers_in_system.qsize() > 0):
            self.num_departures += 1
            old = self.customers_in_system.get()
            self.next_departure = self.dist.exp((1/self.ts))
            return [self.next_departure, old.time_arrival]
        else:
            return 10000


def main():
    ''' just run the setup '''
    args = parser.parse_args()

    test = Controller(args.lam[0], args.ts[0], (2 * args.sim[0]))

    # get and calculate averages
    len_cust = len(test.customer_list) / 2
    len_ts = len(test.ts_list) / 2
    len_lam = len(test.interarrival_list) / 2

    # calculate stats based on measured performance of the system
    queue_mean = (sum(test.customer_list[int(len_cust):]) / len_cust)
    ts_mean = sum(test.ts_list[int(len_ts):]) / len_ts
    lam_mean = sum(test.interarrival_list[int(len_lam):]) / len_lam
    util = (1 / lam_mean) * ts_mean
    q = queue_mean + (util)
    Tq = q / (1 / lam_mean)
    Tw = queue_mean / (1 / lam_mean)


    print()
    print("Analysis at Steady State:")
    print("=========================")
    print()
    print("Avg (mean) of queue: " + str(queue_mean))
    print("Avg (mean) of    Ts: " + str(ts_mean))
    print("Avg (mean) of   Lam: " + str(1/lam_mean))
    print()
    print("util: " + str(util))
    print("   w: " + str(queue_mean) + " customers.")
    print("   q: " + str(q) + " customers.")
    print("  Tq: " + str(Tq) + " seconds.")
    print("  Tw: " + str(Tw) + " seconds.")
    print()
    print("Goodbye! <3")
    print()


if __name__ == "__main__":
    main()
