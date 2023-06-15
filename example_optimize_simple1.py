# Simple optimization example (finding the solution by iteration)
# The waiting times and the number of operators are each assigned a cost.
# The search is for the number of operators for which the costs become minimal.


# Importing modules

# Processing results arrays
import numpy as np

# Simulator
from queuesim import Simulator
from queuesim.tools import SimProcess, run_parallel

# Station types
from queuesim.stations import Source, Process, Dispose
from queuesim.models import mmc_model

# Plot model
import matplotlib.pyplot as plt
import seaborn as sns

# Defining general plot style
sns.set()


# Model parameters

# Arrivals to be simulated
count = 100_000

# Arrival process
mean_I = 50

# Service process
mean_S = 600

# Costs
cost_waiting = 10  # Costs per waiting second
cost_c = 120  # Costs per operator


# Definition of the $x$ range (=number of operators)

c_range = range(14, 25)


if __name__ == '__main__':
    # Parallel simulation of the models
    models, simulators = run_parallel([SimProcess(mmc_model(mean_I, mean_S, c, count)) for c in c_range])

    # Processing results
    waiting_times = np.array([model['Dispose'].statistic_client_waiting.mean for model in models])
    costs = waiting_times * cost_waiting + np.array(c_range) * cost_c

    # Output of results
    print("Cost-optimal number of operators:", c_range[np.argmin(costs)])
    print("Analyzed range:", c_range[0], "...", c_range[-1])

    fig, ax = plt.subplots(figsize=(16, 9))
    ax.plot(c_range, costs)
    ax.set(title="Costs as a function of the number of operators", xlabel="Number of operators $c$", ylabel="Costs")
    plt.show()
