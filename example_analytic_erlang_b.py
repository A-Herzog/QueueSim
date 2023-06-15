# Erlang B (M/M/c/c model)

# There is no waiting room in this model (system size = number of operators).
# If there is no free operator on client arrival, the client will be blocked.
# We have E[W]=0, E[N<sub>Q</sub>]=0, E[V]=E[S] and E[N]/c=&rho;.


# Importing modules

# Erlang module
from queuesim.analytic import erlang_b_table

# Plotting modules
import matplotlib.pyplot as plt
import matplotlib.ticker as formater
import seaborn as sns

# Defining general plot style
sns.set()
percent_formater = formater.PercentFormatter(xmax=1, decimals=0)


# Helper function for plotting Erlang B results

def erlang_b_plot(results, x, title: str, x_label: str, x_is_percent=False) -> None:
    fig, ax = plt.subplots(figsize=(16, 9))

    ax.plot(x, results["P(blocked)"], 'r')
    ax.tick_params(axis='y', labelcolor='r')
    ax.set_xlabel(x_label)
    ax.set_ylabel("P(blocked)", color='r')
    if x_is_percent: ax.xaxis.set_major_formatter(percent_formater)
    ax.yaxis.set_major_formatter(percent_formater)

    ax = ax.twinx()
    ax.plot(x, results["rho_real"], 'g')
    ax.tick_params(axis='y', labelcolor='g')
    ax.set_ylabel("Real utilization $\\rho$", color='g')
    ax.yaxis.set_major_formatter(percent_formater)

    ax.set_title(title)


# P(blocked) as a function of the workload

# Number of operators
c = 10

# Workload range
a_range = range(26)

# Erlang B results for different values of a
results = erlang_b_table([(a, c) for a in a_range])

# Display results table
print(results)


# Plot results

erlang_b_plot(results, results["rho_offered"], "Erlang B model at different offered utilizations", "Offered utilization", True)
plt.show()

# At an offered utilization of 100% about 21% of the arriving clients will be blocked.


# P(blocked) as a function of c

# Now the offered utilization (=a/c) will be fixed at 80%. (a=0.8*c)

# Fixed offered utilization
rho = 0.8

# Number of operators range
c_range = range(1, 21)

# Erlang B results for different values of c
results = erlang_b_table([(0.8 * c, c) for c in c_range])

# Display results table
print(results)


# Plot results

erlang_b_plot(results, results["c"], "Erlang B model at different system sizes", "System size $c$")
plt.show()

# On larger systems it is less likely to be blocked at the same offered utilization (Economy of scale).
# Due to less blocked clients, the real utilization increases.
