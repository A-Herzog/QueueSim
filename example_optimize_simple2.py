
# Simple optimization example (using BOBYQA)
# The waiting times and the number of operators are each assigned a cost.
# The search is for the number of operators for which the costs become minimal.
# BOBYQA documentation: https://numericalalgorithmsgroup.github.io/pybobyqa/build/html/index.html


# Importing modules

# Processing results arrays
import numpy as np

# Optimizer
import pybobyqa

# Simulator
from queuesim.models import mmc_model, get_simulator_from_model


## Model parameters
# Since BOBYQA is slow for the considered problem compared to trying all possible solutions,
# we reduce the number of simulated arrivals by a factor of 10.

# Arrivals to be simulated
count = 10_000

# Arrival process
mean_I = 50

# Service process
mean_S = 600

# Costs
cost_waiting = 10  # Costs per waiting second
cost_c = 120  # Costs per operator


# Definition of the function to be minimized
# The workload (=`meanS/meanI`) is 12, which means that at least 12 operators must be used for the model to reach steady state.
# However, since we generally only simulate significantly less than infinite arrivals, the model will not explode even with a permanent overload.
# Since the number of operators must be an integer, the value is rounded internally, i.e. non-integer values may also be passed.
# The costs are returned, which include the waiting times of the customers and the operators' labor costs.

def f(x):
    global mean_I, mean_S, count, cost_waiting, cost_c
    c = round(x[0])  # c must be an integer
    model = mmc_model(mean_I, mean_S, c, count)
    get_simulator_from_model(model).run()
    waiting_time = model['Dispose'].statistic_client_waiting.mean
    return waiting_time * cost_waiting + c * cost_c


# Running the optimization

# Initial solution
x0 = np.array([15])

# Search range
a = np.array([14])
b = np.array([24])

# Running BOBYQA
soln = pybobyqa.solve(f, x0, bounds=(a, b))


# Results

print("Optimization successful?")
print(soln.flag == soln.EXIT_SUCCESS)
print("")
print(soln)
print("Cost-optimal number of operators:",round(soln.x[0]))
