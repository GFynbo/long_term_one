#
# Gavin Fynbo
# fynbo@bu.edu
# U54777118
#
# This is part4 of the first Long Term Assignment in
# Boston University CAS CS350.
# Prof. Bestavros & Prof. Mancuso
#

import argparse
import heapq
import part3 as cd
import queue
from part1 import RandVar
import random

# parser for dealing with the command line arguments
parser = argparse.ArgumentParser(description='''Process web server simulation using a controller and multiple M/M/1 queues.' +
' Written by Gavin Fynbo, for use in BU CAS CS350''')

class Event:
    ''' This is the class for the structure of the linked list/heap queue of events as to
        hold certain information to be accessed later. '''

    def __init__(self, time_arrival, function_name, queue):
        ''' initialize the Event to get its information '''
        self.time_stamp = time_arrival
        self.function = function_name
        self.queue = queue

class Request:
    ''' This is the class for the structure of the queue of requests as to
        hold certain information to be accessed later by the M/M/1 system. '''

    def __init__(self, time_arrival, time_start):
        ''' initialize the request to get its information '''
        self.time_arrival = time_arrival
        self.time_start = time_start

class Controller:
    ''' This is the controller for the simulated M/M/1 queuing system. This controller
        keeps track of the global timer and global schedule. '''

    def __init__(self, lam, ts, sim_time, p):
        ''' initialize the variables, timer, etc '''
        # read user input to get lambda, time of serice, and simulation time here
        self.lam = lam
        self.ts = ts
        self.sim_time = sim_time

        # keep track of Ts, mean customers in queue
        self.monitor_file = open('monitor_results.txt', 'w')
        # self.interarrival_list = []
        self.dist = RandVar(self.lam)

        # initialize controller main properties here
        self.time = 0
        self.monitor_time = 1
        self.t_p = None
        self.t_s = None
        self.t_f = None
        self.t_i = None
        self.t_o = None
        self.p_s = p[0]
        self.p_i = p[1]
        self.p_a = p[2]

        # keep track of the queues for births and deaths
        # 0 = t_p; 1 = t_s; 2 = t_f; 3 = t_i; 4 = t_o;
        self.queues = [None, None, None, None, None]
        self.queues_stats = [[], [], [], [], []]
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
                self.add_depature_event(event)
            # if monitor call monitor function
            else:
                self.add_monitor_event()
                self.monitor_time += self.dist.exp(5)

    def initialize_state(self):
        ''' initialize the worlds (M/M/1 queues) of the simulation '''
        self.t_p = World(self.lam, self.ts[0])
        self.t_s = World(self.lam, self.ts[1])
        self.t_f = World(self.lam, self.ts[2], True)
        self.t_i = World(self.lam, self.ts[3])
        self.t_o = World(self.lam, self.ts[4])
        self.queues = [self.t_p, self.t_s, self.t_f, self.t_i, self.t_o]

    def initialize_schedule(self):
        ''' initialize the schedule of the simulation '''
        # get first birth and first death and push them onto the schedule
        first_birth = Event(self.t_p.next_arrival, 'birth', 0)
        heapq.heappush(self.schedule, [first_birth.time_stamp, first_birth])
        first_death = Event(self.t_p.next_departure, 'death', 0)
        heapq.heappush(self.schedule, [first_death.time_stamp, first_death])
        # impliment monitor
        first_monitor = Event(self.monitor_time, 'monitor', 0)
        heapq.heappush(self.schedule, [first_monitor.time_stamp, first_monitor])

    def add_arrival_event(self):
        ''' this function simply adds the next arrival event and departure event
            to the heapq at a time time_stamp '''
        birth = self.queues[0].birth(self.time)

        if (len(birth) == 2):
            next_arrival_event = Event(birth[0] + self.time, 'birth', 0)
            heapq.heappush(self.schedule, [next_arrival_event.time_stamp, next_arrival_event])
            return

        next_arrival_event = Event(birth[0] + self.time, 'birth', 0)
        heapq.heappush(self.schedule, [next_arrival_event.time_stamp, next_arrival_event])
        next_departure_event = Event(birth[1] + self.time, 'death', 0)
        heapq.heappush(self.schedule, [next_departure_event.time_stamp, next_departure_event])

    def add_depature_event(self, event):
        ''' this function simply adds the next move or departure event to the heapq at a time time_stamp '''
        death = self.queues[event.queue].death()
        if (death != 10000):
            next_depart = death[1]
            death = death[0]
            next_departure_event = Event(next_depart + self.time, 'death', event.queue)
            heapq.heappush(self.schedule, [next_departure_event.time_stamp, next_departure_event])
            if (event.queue != 4):
                if (event.queue == 0):
                    x = random.random()
                    if (x > self.p_s):
                        move = self.queues[2].move(death.time_arrival, death)
                        next_move_event = Event(move[0] + self.time, 'death', (event.queue + 2))
                        heapq.heappush(self.schedule, [next_move_event.time_stamp, next_move_event])
                    else:
                        move = self.queues[1].move(death.time_arrival, death)
                        next_move_event = Event(move[0] + self.time, 'death', (event.queue + 1))
                        heapq.heappush(self.schedule, [next_move_event.time_stamp, next_move_event])

                elif (event.queue == 1):
                    move = self.queues[event.queue + 1].move(death.time_arrival, death)
                    next_move_event = Event(move[0] + self.time, 'death', (event.queue + 1))
                    heapq.heappush(self.schedule, [next_move_event.time_stamp, next_move_event])

                elif (event.queue == 2):
                    x = random.random()
                    if (x > self.p_i):
                        move = self.queues[event.queue + 2].move(death.time_arrival, death)
                        next_move_event = Event(move[0] + self.time, 'death', (event.queue + 2))
                        heapq.heappush(self.schedule, [next_move_event.time_stamp, next_move_event])
                    else:
                        move = self.queues[event.queue + 1].move(death.time_arrival, death)
                        next_move_event = Event(move[0] + self.time, 'death', (event.queue + 1))
                        heapq.heappush(self.schedule, [next_move_event.time_stamp, next_move_event])

                elif (event.queue == 3):
                    x = random.random()
                    if (x > self.p_a):
                        move = self.queues[event.queue + 1].move(death.time_arrival, death)
                        next_move_event = Event(move[0] + self.time, 'death', (event.queue + 1))
                        heapq.heappush(self.schedule, [next_move_event.time_stamp, next_move_event])
                    else:
                        move = self.queues[event.queue].move(death.time_arrival, death)
                        next_move_event = Event(move[0] + self.time, 'death', (event.queue))
                        heapq.heappush(self.schedule, [next_move_event.time_stamp, next_move_event])

    def add_monitor_event(self):
        ''' this method impliments a monitoring event that captures the system in
            its current state, including number of customers in the queue, the
            amount of departures and the amout of arrivals '''
        # COME BACK TO PUT MONITOR IN PLACE
        next_departure_event = Event(self.monitor_time, 'monitor', 0)
        heapq.heappush(self.schedule, [next_departure_event.time_stamp, next_departure_event])
        for i in range(len(self.queues)):
            self.queues_stats[i] += [self.queues[i].customers_in_system.qsize()]
        # stats = [self.world.customers_in_system.qsize(), self.world.num_arrivals, self.world.num_departures]
        # self.monitor_file.write("Monitor at: " + str(self.time) + " \nCustomers in queue: " + str(stats[0]) + " \nArrivals: " + str(stats[1]) + " \nDepartures: " + str(stats[2]) + " \n\n")

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

    def __init__(self, lam=1, ts=0.5, custom_dist=False):
        ''' initialize the world simulator for specific variables such as
            arrival rate, time to service and the total simulation time '''

        # for generating arrival and departure times
        self.lam = lam
        self.ts = ts
        self.custom_dist = custom_dist

        # monitoring purposes
        self.num_arrivals = 0
        self.num_departures = 0
        self.service_times = []

        # create the queue for M/M/1
        self.customers_in_system = queue.Queue()

        # for calculating the initial arrival and departure time
        self.dist = RandVar(self.lam)
        self.next_arrival = self.dist.exp()
        self.next_departure = 0

        # check if it uses a custom or exponential distribution
        if (self.custom_dist):
            self.next_departure = cd.customDistr(self.ts)
        else:
            self.next_departure = self.next_arrival + self.dist.exp((1/self.ts))

    def birth(self, time_arrival=0):
        ''' the birth of an event to be added into M/M/1 Queue and the birth and
            death events to be added into the simulation schedule '''
        req = Request(time_arrival, time_arrival)
        self.customers_in_system.put(req)
        self.num_arrivals += 1
        self.next_arrival = self.dist.exp(self.lam)
        if (self.customers_in_system.qsize() <= 1):
            self.next_departure = self.next_arrival + self.dist.exp((1/self.ts))
            return [self.next_arrival, self.next_departure, req]
        return [self.next_arrival, req]

    def move(self, time_arrival, old):
        ''' simply add a request from the old queue to this queue '''
        self.customers_in_system.put(old)
        self.num_arrivals += 1
        # return the custom distribution if that's what it requires
        if self.custom_dist:
            self.next_move = self.dist.exp(1 / cd.customDistr(self.ts))
        else:
            self.next_move = self.dist.exp((1/self.ts))

        return [self.next_move]

    def death(self):
        ''' the death of an event to be removed from the M/M/1 Queue '''
        if (self.customers_in_system.qsize() > 0):
            self.num_departures += 1
            self.next_departure = self.calc_depart()
            return [self.customers_in_system.get(), self.next_departure]

        else:
            return 10000

    def calc_depart(self):
        ''' just do the math for the departure '''
        # check if it uses a custom or exponential distribution
        if (self.custom_dist):
            self.next_departure = self.next_arrival + cd.customDistr(self.ts)
            self.service_times += [self.next_departure - self.next_arrival]
            return (self.next_departure)
        else:
            self.next_departure = self.next_arrival + self.dist.exp((1/self.ts))
            self.service_times += [self.next_departure - self.next_arrival]
            return (self.next_departure)

def main():
    ''' just run the setup '''
    args = parser.parse_args()
    # for the sake of the web server simulation we will just hard code the input
    # information into the controller
    ts_table = [[0.03, 0.03],
                [0.06, 0.07],
                [0.08, 0.10],
                [0.10, 0.40],
                [0.13, 0.20],
                [0.19, 0.11],
                [0.22, 0.08],
                [0.30, 0.01]]
    ts_list = [0.005, 0.010, ts_table, 0.045, 0.012]
    p_list = [0.8, 0.35, 0.10]
    test = Controller(10, ts_list, (2000), p_list)

    q_means = [0, 0, 0, 0, 0]
    q_utils = [0, 0, 0, 0, 0]
    for i in range(5):
        q_means[i] = sum(test.queues_stats[i])/len(test.queues_stats[i])
        q_utils[i] = sum(test.queues[i].service_times)/len(test.queues[i].service_times) * (10)

    print(q_means)
    print(q_utils)

if __name__ == "__main__":
    main()
