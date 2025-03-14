# More detailed optimization example (using BOBYQA)
# There are costs associated with waiting times.
# In addition, the operation of the system costs money depending on the time.
# Each successfully served client brings in a fixed profit. The number of orders accepted per day can be controlled.
# BOBYQA documentation: https://numericalalgorithmsgroup.github.io/pybobyqa/build/html/index.html


# Importing modules

# Processing results arrays
import numpy as np

# Optimizer
import pybobyqa

# Simulator
from queuesim.models import mmc_model, get_simulator_from_model


# Model parameters

# Arrivals to be simulated
count = 100_000

# Service process
mean_S = 80
c = 1

# Costs
profit_per_client = 100  # Revenue per customer served
cost_waiting = 0.02  # Costs per waiting second
operation_cost_per_second = 0.5


# Definition of the function to be minimized

def f(x):
    # Generate model
    global mean_S, c, count, profit_per_client, cost_waiting, operation_cost_per_second
    rho = x[0]
    mean_I = mean_S / rho / c
    model = mmc_model(mean_I, mean_S, c, count)

    # Simulation
    get_simulator_from_model(model).run()

    # Calculate auxiliary result variables
    waiting_time = model['Dispose'].statistic_client_waiting.mean
    clients_per_day = model['Source'].count / model['Process'].statistic_wip.time * 86400
    yield_per_client = profit_per_client - waiting_time * cost_waiting

    # Revenue
    return clients_per_day * yield_per_client - operation_cost_per_second * 86400


def minimize_f(x):
    return -f(x)


# Running the optimization

# Initial solution
x0 = np.array([0.75])

# Search range
a = np.array([0.5])
b = np.array([0.99])

# Running BOBYQA
soln = pybobyqa.solve(minimize_f, x0, bounds=(a, b))  # Actually corrent, but then the optimization runs endlessly (==">5Min"):  objfun_has_noise=True


# Results

print("Optimization successful?")
print(soln.flag == soln.EXIT_SUCCESS)

print(soln)

print("Result (should be 88.8%)")
print(round(soln.x[0] * 100, 1), "%")

x = np.linspace(soln.x[0] - 0.02, soln.x[0] + 0.02, 20)
y = [f([float(rho)]) for rho in x]  # Takes a little longer, quite simpile formulation without parallelization (approx. 1 min on fast machine)

print("Verification per iteration via [y-epsilon, y+epsilon]")
print(round(x[np.argmax(y)][0] * 100, 1), "%")

# Attention: $f(x)$ is not deterministic.
# If the iterative search returns a slightly different value, this does not mean that the optimization result is not the optimum.
