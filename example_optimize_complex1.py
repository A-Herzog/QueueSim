# More detailed optimization example (finding the solution by iteration)
# There are costs associated with waiting times.
# In addition, the operation of the system costs money depending on the time.
# Each successfully served client brings in a fixed profit. The number of orders accepted per day can be controlled.


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

# Service process
mean_S = 80
c = 1

# Costs
profit_per_client = 100  # Revenue per customer served
cost_waiting = 0.02  # Costs per waiting second
operation_cost_per_second = 0.5


# Definition of the $x$ range (=Zwischenankunftszeiten)

mean_I_range = range(81, 141)


if __name__ == '__main__':
    # Parallel simulation of the models
    models, simulators = run_parallel([SimProcess(mmc_model(mean_I, mean_S, c, count)) for mean_I in mean_I_range])

    # Processing results

    # Utilization of the operators
    rho = np.array([model['meanS'] / model['meanI'] / model['c'] for model in models])

    # Mean waiting times
    waiting_times = np.array([model['Dispose'].statistic_client_waiting.mean for model in models])

    # Served client per day
    clients_per_day = np.array([model['Source'].count / model['Process'].statistic_wip.time * 86400 for model in models])

    # Revenue per client
    yield_per_client = profit_per_client - waiting_times * cost_waiting

    # Revenue per day
    yield_per_day = clients_per_day * yield_per_client - operation_cost_per_second * 86400

    # Output of results
    print("Cost-optimal utilization of the operators: \N{greek small letter rho}=", round(rho[np.argmax(yield_per_day)] * 100, 1), "%")
    print("Analyzed range:", round(min(rho) * 100, 1), "% ...", round(max(rho) * 100, 1), "%")

    fig, ax = plt.subplots(figsize=(16, 9))
    ax.plot(rho, yield_per_day)
    ax.set_ylim([0, max(yield_per_day) * 1.05])
    ax.set(title="Revenue as a function of the utilization of the operators", xlabel="Utilization $\\rho$", ylabel="Revenue")
    plt.show()
