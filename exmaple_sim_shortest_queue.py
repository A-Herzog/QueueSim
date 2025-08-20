# Queueing system with control
# Decide stations can branch clients by using lambda functions. In the following model the clients are sent to one of two process stations depending on the queue lengths at the corresponding stations.


# Importing modules

# Generating integer pseudo random numbers
from random import randint

# Collecting results
import pandas as pd

# Simulation
from queuesim.stations import Source, Decide, DecideCondition, Process, Dispose
from queuesim import Simulator
from queuesim.random_dist import exp as exp_dist


# General model parameters

# Arrivals to be simulated
count = 100_000

# Inter-arrival times distribution
inter_arrival_time = exp_dist(50)

# Service times distribution
process_time = exp_dist(80)

# Fast service times distribution
process_time_fast = exp_dist(40)

# Number of operators per service station (by using two stations)
c = 1


# Prepare data collection

enq_dict = {}
en_dict = {}


# Two stations with individual queues, new clients choosing the queue by change

# Simulator
simulator = Simulator()

# Stations
source = Source(simulator, count, inter_arrival_time)
decide = Decide(simulator)
process1 = Process(simulator, process_time, c)
process2 = Process(simulator, process_time, c)
dispose = Dispose(simulator)

# Link stations
source.set_next(decide)
decide.add_next(process1, 1)
decide.add_next(process2, 1)
process1.set_next(dispose)
process2.set_next(dispose)

# Run simulation
simulator.run()

# Results
name = "2 queues, random"
enq = process1.statistic_queue_length.mean + process2.statistic_queue_length.mean
en = process1.statistic_wip.mean + process2.statistic_wip.mean
enq_dict[name] = enq
en_dict[name] = en
print("")
print("Two stations with individual queues, new clients choosing the queue by change")
print("E[NQ]=", round(enq, 2), sep="")
print("E[N]=", round(en, 2), sep="")


# Two stations with individual queues, new clients will enter the shortest queue

# Simulator
simulator = Simulator()

# Stations
source = Source(simulator, count, inter_arrival_time)
decide = DecideCondition(simulator)
process1 = Process(simulator, process_time, c)
process2 = Process(simulator, process_time, c)
dispose = Dispose(simulator)

def shortest_queue(client) -> int:
    nq1 = process1.nq
    nq2 = process2.nq
    if nq1 < nq2: return 0
    if nq1 > nq2: return 1
    return randint(0, 1)

# Link stations
source.set_next(decide)
decide.set_condition(shortest_queue)
decide.add_next(process1)
decide.add_next(process2)
process1.set_next(dispose)
process2.set_next(dispose)

# Run simulation
simulator.run()

# Results
name = "2 queues, shortest"
enq = process1.statistic_queue_length.mean + process2.statistic_queue_length.mean
en = process1.statistic_wip.mean + process2.statistic_wip.mean
enq_dict[name] = enq
en_dict[name] = en
print("")
print("Two stations with individual queues, new clients will enter the shortest queue")
print("E[NQ]=", round(enq, 2), sep="")
print("E[N]=", round(en, 2), sep="")


# One service station (with a single queue) with two parallel operators at the station

# Simulator
simulator = Simulator()

# Stations
source = Source(simulator, count, inter_arrival_time)
process = Process(simulator, process_time, 2 * c)
dispose = Dispose(simulator)

# Link stations
source.set_next(process)
process.set_next(dispose)

# Run simulation
simulator.run()

# Results
name = "1 queue, 2 parallel operators"
enq = process.statistic_queue_length.mean
en = process.statistic_wip.mean
enq_dict[name] = enq
en_dict[name] = en
print("")
print("One service station (with a single queue) with two parallel operators at the station")
print("E[NQ]=", round(enq, 2), sep="")
print("E[N]=", round(en, 2), sep="")


# One service station (with a single queue) with batch processing

# Simulator
simulator = Simulator()

# Stations
source = Source(simulator, count, inter_arrival_time)
process = Process(simulator, process_time, c, b=2)
dispose = Dispose(simulator)

# Link stations
source.set_next(process)
process.set_next(dispose)

# Run simulation
simulator.run()

# Results
name = "1 queue, batch processing"
enq = process.statistic_queue_length.mean
en = process.statistic_wip.mean
enq_dict[name] = enq
en_dict[name] = en
print("")
print("One service station (with a single queue) with batch processing")
print("E[NQ]=", round(enq, 2), sep="")
print("E[N]=", round(en, 2), sep="")


# One service station (with a single queue) with a twice as fast operator as on the other models

# Simulator
simulator = Simulator()

# Stations
source = Source(simulator, count, inter_arrival_time)
process = Process(simulator, process_time_fast, c)
dispose = Dispose(simulator)

# Link stations
source.set_next(process)
process.set_next(dispose)

# Run simulation
simulator.run()

# Results
name = "1 queue, fast operator"
enq = process.statistic_queue_length.mean
en = process.statistic_wip.mean
enq_dict[name] = enq
en_dict[name] = en
print("")
print("One service station (with a single queue) with a twice as fast operator as on the other models")
print("E[NQ]=", round(enq, 2), sep="")
print("E[N]=", round(en, 2), sep="")


# Results of all models
results = pd.DataFrame({'E[NQ]': enq_dict, 'E[N]': en_dict})
print(results)

# All 5 models have the same arrival rate and the same operating capacity.
# In terms of queue lengths (or waiting time) the two queues with random selection is worst.
# Batch processing at a single station is a bit better, selecting the shortest of two queues is even more better.
# A single process station with a single fast operator is quite good. But a single process station with two operators is even better (in terms of queue length).
# Because in this case, if a client is already in process, if a second client arrives, this can be served immediately, too.
# In the case of the single, fast operator this second client would have to wait a short time.

# When considering the average number of clients in the system, the model with the fast operator is the best.
# In this model, the average waiting times are a bit longer than in the model with the two parallel operators at a single station.
# But because the processing times are significantly shorter, the average number of clients (waiting and in process) in the system is lower.
