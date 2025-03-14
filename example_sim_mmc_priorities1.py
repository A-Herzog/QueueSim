# Comparing different queueing disciplines


# Importing modules

# Generating random priorities
from random import random as random_float

# Simulation
from queuesim.models import mmc_model_priorities, get_simulator_from_model


# Model parameters

# Mean inter-arrival time
mean_i = 100

# Mean service time
mean_s = 80

# Number of operators
c = 1

# Number of arrivals to be simulated
count = 500_000


# Priority formulas
# The client with the highest priority will be served next. So using the waiting time as priority will lead to FIFO, using -waiting time is LIFO.

def priority_FIFO(client, waiting_time):
    return waiting_time


def priority_LIFO(client, waiting_time):
    return -waiting_time


def priority_random(client, waiting_time):
    return random_float() * 100

# For FIFO and LIFO no priority lambda expressions are needed. FIFO and LIFO can be defined at the process station directly.
# In this example the lambda expressions for all three options were defined only for symmetry reasons.


# Simulation

def run_simulation(mean_i, mean_s, c, count, priority, priority_name):
    # Build model
    model = mmc_model_priorities(mean_i, mean_s, c, count, priority)

    # Run simulation
    simulator = get_simulator_from_model(model)
    simulator.run()

    # Show results
    print(priority_name)
    dispose = model['Dispose']
    print("  Service times (S): " + dispose.statistic_client_service.info)
    print("  Residence times (V): " + dispose.statistic_client_residence.info)
    print("  Waiting times (W): " + dispose.statistic_client_waiting.info)
    print()


run_simulation(mean_i, mean_s, c, count, priority_FIFO, "FIFO")
run_simulation(mean_i, mean_s, c, count, priority_random, "Random")
run_simulation(mean_i, mean_s, c, count, priority_LIFO, "LIFO")

# The queueing discipline is not influencing the mean waiting times but the coefficient of variation of the waiting times:
# On FIFO CV[W] is about 1.2
# On random service order CV[W] is about 1.7 - 1.8
# On LIFO CV[W] is 3.5 or more
