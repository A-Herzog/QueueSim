# Erlang C (M/M/c model)
# This is an implementation of the default Erlang C model (exponential inter-arrival and service times, `c` operators).


# Importing modules

# Erlang module
from queuesim.analytic import erlang_c_table

# Plotting modules
import matplotlib.pyplot as plt
import matplotlib.ticker as formater

# Defining general plot style
plt.style.use('seaborn-v0_8')
percent_formater = formater.PercentFormatter(xmax=1, decimals=0)


# Mean waiting time as a function of &rho;

# Arrival rate range
l_range = [1 / mean_i for mean_i in range(61, 85)]

# Service rate
mu = 1 / 600

# Number of operators
c = 10

# Erlang C results for different values of lambda
results = erlang_c_table([(l, mu, c) for l in l_range])

# Display results table
print(results)


# Plot results

_, ax = plt.subplots(figsize=(16, 9))

ax.plot(results["rho"], results["E[W]"], 'r')
ax.tick_params(axis='y', labelcolor='r')
ax.set_xlabel("Utilization $\\rho$")
ax.set_ylabel("E[W]", color='r')
ax.xaxis.set_major_formatter(percent_formater)

ax.set_title("Erlang C model at different utilizations")
plt.show()


# Mean waiting time as a function of c
# Now the utilization will be fixed at &rho;=80%.
# The service rate will also stay fixed at &mu;=1/600.
# The arrival rate will be adjusted when changing c to keep &rho; fixed: &lambda;=&rho;*&mu;*c.

# Fixed utilization
rho = 0.8

# Service rate
mu = 1 / 600

# Number of operators range
c_range = range(1, 26)

# Erlang C results for different values of c
results = erlang_c_table([(rho * mu * c, mu, c) for c in c_range])

# Display results table
print(results)


# Plot results

_, ax = plt.subplots(figsize=(16, 9))

ax.plot(results["c"], results["E[W]"], 'r')
ax.tick_params(axis='y', labelcolor='r')
ax.set_xlabel("Number of operators $c$")
ax.set_ylabel("E[W]", color='r')

ax = ax.twinx()
ax.plot(results["c"], results["rho"], 'g')
ax.tick_params(axis='y', labelcolor='g')
ax.set_ylabel("Utilization $\\rho$", color='g')
ax.yaxis.set_major_formatter(percent_formater)

ax.set_title("Erlang C model at different numbers of operators (and the same utilization in all cases)")
plt.show()

# On a larger system (with more operators) the mean waiting time will be lower (at the same utilization) (Economy of scale).
