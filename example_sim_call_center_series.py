# Different aspects of a complex call center model


# Importing modules

# Data collection
import pandas as pd

# Plotting modules
import matplotlib.pyplot as plt
import matplotlib.ticker as formater
import seaborn as sns

# Simulation
from queuesim import SimProcess, run_parallel
from queuesim.models import impatience_and_retry_model_build

# Analytic calcution
from queuesim.analytic import erlang_c_table, erlang_c_ext_table

# Defining general plot style
sns.set()
percent_formater = formater.PercentFormatter(xmax=1, decimals=0)


# Impatience of the callers

# Mean inter-arrival time
mean_i = 100

# Mean service time
mean_s_range = range(60, 121, 2)

# Mean waiting time tolerance range
mean_wt = 300

# Number of operators
c = 1

# Number of arrivals to be simulated
count = 100_000

if __name__ == '__main__':
    # Simulation
    models, simulators = run_parallel([SimProcess(impatience_and_retry_model_build(mean_i, mean_s, mean_wt, 0, 1, c, count)) for mean_s in mean_s_range])

    # Processing results
    mu = [1 / model['meanS'] for model in models]
    rho_offered = [model['meanS'] / model['meanI'] / model['c'] for model in models]
    ENQ = [model['Process'].statistic_queue_length.mean for model in models]
    EN = [model['Process'].statistic_wip.mean for model in models]
    EW = [model['Dispose'].statistic_client_waiting.mean for model in models]
    EV = [model['Dispose'].statistic_client_residence.mean for model in models]
    PA = [1 - model['Process'].statistic_success.data['Success'] / model['Process'].statistic_success.count for model in models]

    results = pd.DataFrame({'mu': mu, 'rho_offered': rho_offered, 'E[N_Q]': ENQ, 'E[N]': EN, 'E[W]': EW, 'E[V]': EV, 'P(A)': PA})
    print("")
    print("Impatience of the callers")
    print(results)

    # Calculating Erlang C formula results
    erlang_c_results = erlang_c_table([(1 / mean_i, mu, c) for mu in results[results["rho_offered"] < 1]["mu"]])
    erlang_c_ext_results = erlang_c_ext_table([(1 / mean_i, mu, 1 / mean_wt, c, c * 100) for mu in results["mu"]])

    # Plotting results
    fig, ax = plt.subplots(figsize=(16, 9))

    ax.plot(results['rho_offered'], results['E[W]'], 'r', label="E[W] simulation results")
    ax.plot(erlang_c_results['rho'], erlang_c_results['E[W]'], 'k', label="E[W] Erlang C formula results")
    ax.plot(erlang_c_ext_results['rho_offered'], erlang_c_ext_results['E[W]'], 'b', label="E[W] extended Erlang C formula results")
    ax.xaxis.set_major_formatter(percent_formater)
    ax.set_ylim([0, max(results['E[W]'] * 1.5)])
    ax.set_xlabel("Offered utilization")
    ax.set_ylabel("Mean waiting time E[W]")
    lines1, labels1 = ax.get_legend_handles_labels()

    ax2 = ax.twinx()
    ax2.plot(results['rho_offered'], results['P(A)'], 'r:', label="P(A) simulation results")
    ax2.plot(erlang_c_ext_results['rho_offered'], erlang_c_ext_results['P(A)'], 'b:', label="P(A) extended Erlang C formula results")
    ax2.yaxis.set_major_formatter(percent_formater)
    ax2.set_ylabel("Waiting cancel probability P(A)")
    lines2, labels2 = ax2.get_legend_handles_labels()

    ax.set_title("Mean waiting time as a function of the utilization")
    ax.legend(lines1 + lines2, labels1 + labels2)
    plt.show()

    # Calculating E[W] using the simple Erlang C formula (not respecting the impatience) gives completely wrong results.
    # So the effect of impatience cannot be ignored. The extended Erlang C formula and the simulation results have a good match.
    # We see the waiting time cancelation probability P(A) is increasing at an increasing offered utilization.
    # The mean waiting time E[W] is also increasing but not in the same magnitude as it would without impatience.
    # If there are waiting time cancelations, the system can also be operated with an offered utilization of more than 100%.


# Retry

# Mean inter-arrival time
mean_i = 100

# Mean service time
mean_s_range = range(60, 121, 2)

# Mean waiting time tolerance range
mean_wt = 300

# Retry
retry_probability = 0.2
mean_retry_delay = 600

# Number of operators
c = 1

# Number of arrivals to be simulated
count = 100_000

if __name__ == '__main__':
    # Simulation
    models, simulators = run_parallel([SimProcess(impatience_and_retry_model_build(mean_i, mean_s, mean_wt, retry_probability, mean_retry_delay, c, count)) for mean_s in mean_s_range])

    # Processing results
    mu = [1 / model['meanS'] for model in models]
    rho_offered = [model['meanS'] / model['meanI'] / model['c'] for model in models]
    ENQ = [model['Process'].statistic_queue_length.mean for model in models]
    EN = [model['Process'].statistic_wip.mean for model in models]
    EW = [model['Dispose'].statistic_client_waiting.mean for model in models]
    EV = [model['Dispose'].statistic_client_residence.mean for model in models]
    PA = [1 - model['Process'].statistic_success.data['Success'] / model['Process'].statistic_success.count for model in models]

    results = pd.DataFrame({'mu': mu, 'rho_offered': rho_offered, 'E[N_Q]': ENQ, 'E[N]': EN, 'E[W]': EW, 'E[V]': EV, 'P(A)': PA})
    print("")
    print("Retry")
    print(results)

    # Calculating Erlang C formula results
    erlang_c_ext_results = erlang_c_ext_table([(1 / mean_i, mu, 1 / mean_wt, c, c * 100) for mu in results["mu"]])

    # Using the simple Erlang C formula was already in the model above no good idea anymore.
    # So when adding also retry, we have left of the simple Erlang C formula here.
    # The extended Erlang C formula can handle impatience but no retry.
    # So deviations between the simulation and the formula results can be expected.

    # Plotting results
    fig, ax = plt.subplots(figsize=(16, 9))

    ax.plot(results['rho_offered'], results['E[W]'], 'r', label="E[W] simulation results")
    ax.plot(erlang_c_ext_results['rho_offered'], erlang_c_ext_results['E[W]'], 'b', label="E[W] extended Erlang C formula results")
    ax.xaxis.set_major_formatter(percent_formater)
    ax.set_ylim([0, max(results['E[W]'] * 1.5)])
    ax.set_xlabel("Offered utilization")
    ax.set_ylabel("Mean waiting time E[W]")
    lines1, labels1 = ax.get_legend_handles_labels()

    ax2 = ax.twinx()
    ax2.plot(results['rho_offered'], results['P(A)'], 'r:', label="P(A) simulation results")
    ax2.plot(erlang_c_ext_results['rho_offered'], erlang_c_ext_results['P(A)'], 'b:', label="P(A) extended Erlang C formula results")
    ax2.yaxis.set_major_formatter(percent_formater)
    ax2.set_ylabel("Waiting cancel probability P(A)")
    lines2, labels2 = ax2.get_legend_handles_labels()

    ax.set_title("Mean waiting time as a function of the utilization")
    ax.legend(lines1 + lines2, labels1 + labels2)
    plt.show()

    # Only 20% of the callers who have canceled waiting are staring a new call attempt later.
    # This increases the average waiting times as can be seen significantly compared to the
    # results of the extended Erlang C formula (which does not map retry).
