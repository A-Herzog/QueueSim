# Parameter series for M/M/c model
# This example shows the effect of different average service times in a M/M/c model on the waiting times.


# Importing modules

# Data collection
import pandas as pd

# Plotting modules
import matplotlib.pyplot as plt
import matplotlib.ticker as formater
import seaborn as sns

# Simulation
from queuesim import SimProcess, run_parallel, get_multi_run_info
from queuesim.models import mmc_model

# Analytic calcution
from queuesim.analytic import erlang_c_table

# Defining general plot style
sns.set()


# Model parameters

# Mean inter-arrival time
mean_i = 100

# Mean service time range
mean_s_range = range(70, 93)

# Number of operators
c = 1

# Number of arrivals to be simulated
count = 100_000


if __name__ == '__main__':

    # Parallel simulation of the M/M/c models with E[I]=100, c=1 and E[S]=70,71,...,92 each with 100,000 arrivals
    models, simulators = run_parallel([SimProcess(mmc_model(mean_i, mean_s, c, count)) for mean_s in mean_s_range])

    # Processing results
    mu = [1 / model['meanS'] for model in models]
    rho = [model['meanS'] / model['meanI'] / model['c'] for model in models]
    ENQ = [model['Process'].statistic_queue_length.mean for model in models]
    EN = [model['Process'].statistic_wip.mean for model in models]
    EW = [model['Dispose'].statistic_client_waiting.mean for model in models]
    EV = [model['Dispose'].statistic_client_residence.mean for model in models]
    results = pd.DataFrame({'mu': mu, 'rho': rho, 'E[N_Q]': ENQ, 'E[N]': EN, 'E[W]': EW, 'E[V]': EV})
    print(results)

    # Calculating Erlang C formula results
    parameter = [(1 / mean_i, mu, c) for mu in results["mu"]]
    erlang_c_results = erlang_c_table(parameter)

    # Simulation runtimes
    print(get_multi_run_info([model['Source'] for model in models], simulators))
    print("total = Maximum of the computing times of the individual processes")
    print("real = Computing time per client on a single CPU core (dividing this value by the number of CPU cores is total output)")

    # Plotting results
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.plot(results['rho'], results['E[W]'], 'b', label="Simulation results")
    ax.plot(erlang_c_results['rho'], erlang_c_results['E[W]'], 'r', label="Erlang C formula results")
    ax.xaxis.set_major_formatter(formater.PercentFormatter(xmax=1, decimals=0))
    ax.set_xlabel("Utilization $\\rho$")
    ax.set_ylabel("Mean waiting time E[W]")
    ax.legend()
    ax.set_title("Mean waiting time as a function of the utilization")
    plt.show()
