# Extended Erlang C (M/M/c/K+M model)
# This is an Erlang C model with impatient clients.


# Importing modules

# Erlang module
from queuesim.analytic import erlang_c_ext_table

# Plotting modules
import matplotlib.pyplot as plt
import matplotlib.ticker as formater

# Defining general plot style
plt.style.use('seaborn-v0_8')
percent_formater = formater.PercentFormatter(xmax=1, decimals=0)


# Mean waiting time as a function of &rho;

# Arrival rate range
l_range = [1 / mean_i for mean_i in range(40, 75, 2)]

# Service rate
mu = 1 / 600

# Waiting cancelation rate
nu = 1 / 900

# Number of operators
c = 10

# System size
K = 20

# Erlang C results for different values of lambda
results = erlang_c_ext_table([(l, mu, nu, c, K) for l in l_range])

# Display results table
print(results)


# Plot results

_, ax = plt.subplots(figsize=(16, 9))

line1 = ax.plot(results["rho_offered"], results["E[W]"], 'b', label="E[W]")
ax.tick_params(axis='y', labelcolor='b')
ax.set_xlabel("Offered utilization")
ax.set_ylabel("E[W]", color='b')
ax.xaxis.set_major_formatter(percent_formater)
lines1, labels1 = ax.get_legend_handles_labels()

ax = ax.twinx()
line2 = ax.plot(results["rho_offered"], results["P(A)"], 'r', label="P(A) (waiting cancelations)")
line3 = ax.plot(results["rho_offered"], results["P(blocked)"], 'r--', label="P(blocked) (blocked clients)")
line4 = ax.plot(results["rho_offered"], results["rho_real"], 'g', label="$\\rho$ (real utilization)")
ax.set_ylabel("P(A) and $\\rho$")
ax.yaxis.set_major_formatter(percent_formater)
lines2, labels2 = ax.get_legend_handles_labels()

ax.set_title("Extended Erlang C model at different utilizations")
ax.legend(lines1 + lines2, labels1 + labels2)
plt.show()
